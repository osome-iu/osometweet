import requests
import pause
from typing import Union
from datetime import datetime

from .oauth import OAuthHandler
from .fields import ObjectFields, ObjectFieldsBase, UserFields, TweetFields, MediaFields, PollFields, PlaceFields
from .expansions import ObjectExpansions, TweetExpansions, UserExpansions

from osometweet.utils import get_logger, pause_until

logger = get_logger(__name__)


class OsomeTweet:
    def __init__(
        self,
        oauth: OAuthHandler,
        base_url: str = "https://api.twitter.com/2",
    ) -> None:
        self._oauth = oauth
        # A lot of endpoints can only receive payload paremeters specific
        # to their endpoint, initializing with all of the different objects
        # will lead to a 401 error if we have unnecessary objects so we can
        # solve this simply by initializing with an empty dictionary
        # and updating self._params for each method.
        self._base_url = base_url
        self._params = {}

    ########################################
    ########################################
    # Helper functions
    def set_base_url(self, base_url: str) -> None:
        """
        Sets the APIs base URL. The URL for API v2 is https://api.twitter.com/2/<endpoint>

        Parameters:
            - base_url (str) - base url of the api
        Returns:
            - None
        Raises:
            - ValueError
        """
        if isinstance(base_url, str):
            self._base_url = base_url
        else:
            raise ValueError("Invalid type for parameter base_url, must be a string")

    def _decorate_payload(
            self,
            payload: dict = None,
            endpoint_type: str = None,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: ObjectExpansions = None
        ) -> dict:
        """
        Method to add fields and expansions to the payload.
        If the `everything` is set to True, then all optional fields and expansions will be returned regardless of the values of `fields` and `expansions`.

        Parameters:
            - payload: (dict) - the payload
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (TweetExpansions) - Expansions enable requests to expand an ID into a full object in the response. (default = None)

        Returns:
            - dict
        """
        if payload is None:
            payload = dict()

        if everything:
            if endpoint_type == 'user':
                fields = sum([
                    TweetFields(everything=True),
                    UserFields(everything=True)
                ])
                expansions = UserExpansions()
            elif endpoint_type == 'tweet':
                fields = sum([
                    TweetFields(everything=True),
                    UserFields(everything=True),
                    MediaFields(everything=True),
                    PollFields(everything=True),
                    PlaceFields(everything=True)
                ])
                expansions = TweetExpansions()
            else:
                logger.error("Invalid endpoint type, must be 'user' or 'tweet'.")

        # Include expansions if present
        if expansions is not None:
            payload.update(expansions.expansions_object)
        # Include fields if present
        if fields is not None:
            payload.update(fields.fields_object)
        return payload

    ########################################
    ########################################
    # Tweet endpoints
    def tweet_lookup(
            self,
            tids: Union[str, list, tuple],
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: TweetExpansions = None
        ) -> dict:
        """
        Looks-up at least one tweet using its tweet id.
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets

        Parameters:
            - tids: (str, list, tuple) - Up to 100 unique tweet ids.
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (TweetExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
        
        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        if isinstance(tids, (str)):
            payload = {"ids": tids}
        elif isinstance(tids, (list, tuple)):
            if len(tids) > 100:
                raise Exception("Number of tweet ids exceeds maximum of 100")
            payload = {"ids": ",".join(tids)}
        else:
            raise ValueError(
                "Invalid type for parameter 'tids', must be a string, list, or tuple"
            )

        # Set url and update payload with params
        url = f"{self._base_url}/tweets"
        payload = self._decorate_payload(
            payload=payload,
            endpoint_type='tweet',
            everything=everything,
            fields=fields,
            expansions=expansions
        )
        response = self._oauth.make_request(url, payload)
        return response.json()

    def get_tweet_timeline(
            self,
            user_id: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Returns Tweets composed by a single user, specified by the requested user ID.
            - Max: 3200 most recent tweets (using pagination_token)
            - Default: 10 most recent tweets (tweet_id and text data fields only)
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "end_time", "until_it" and "pagination_token"

        Available kwargs:
            - end_time (date (ISO 8601)): The newest or most recent UTC timestamp from
                which the Tweets will be provided. Does not override 3200 limit. Has
                second granularity, and is inclusive of that second. Minimum allowable
                time is 2010-11-06T00:00:00Z.
            - exclude ("retweets" and/or "replies") : Comma-separated list of the types
                of Tweets to exclude from the response. "retweets" still returns max of
                3200 tweets. If "replies" included, only the most recent 800 tweets are
                returned.
            - max_results (int) : The number of tweets to try and retrieve, up to a
                maximum = 100 per distinct request. Otherwise, 10 is returned per
                request. Minimum = 5.
            - pagination_token (str) :  This parameter is used to move forwards or
                backwards through 'pages' of results, based on the value of the
                next_token or previous_token in the response. (E.g., after executing
                `response = get_tweet_timeline()`, `next_token` can be found with
                `response["meta"]["next_token"]`)
            - start_time (date (ISO 8601)) : The oldest or earliest UTC timestamp
                from which the Tweets will be provided. Does not override 3200 limit.
                Has second granularity, and is inclusive of that second. Minimum
                allowable time is 2010-11-06T00:00:00Z.
            - until_id (str) : Returns results with a tweet ID less less than (that
                is, older than) the specified 'until' tweet ID. Results will exclude the
                tweet ID provided. Does not override 3200 limit.

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        return self._timeline_lookup(user_id, "tweets", everything=everything, fields=fields, expansions=expansions, **kwargs)

    def get_mentions_timeline(
            self,
            user_id: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Returns Tweets mentioning a single user specified by the requested user ID.
            - Max: 800 most recent tweets (using pagination_token)
            - Default: 10 most recent tweets (tweet_id and text data fields only)
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-mentions

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"

        Available kwargs:
            - end_time (date (ISO 8601)): The newest or most recent UTC timestamp from
                which the Tweets will be provided. Does not override 3200 limit. Has
                second granularity, and is inclusive of that second. Minimum allowable
                time is 2010-11-06T00:00:00Z.
            - exclude ("retweets" and/or "replies") : Comma-separated list of the types
                of Tweets to exclude from the response. "retweets" still returns max of
                3200 tweets. If "replies" included, only the most recent 800 tweets are
                returned.
            - max_results (int) : The number of tweets to try and retrieve, up to a
                maximum = 100 per distinct request. Otherwise, 10 is returned per
                request. Minimum = 5.
            - pagination_token (str) :  This parameter is used to move forwards or
                backwards through 'pages' of results, based on the value of the
                next_token or previous_token in the response. (E.g., after executing
                `response = get_tweet_timeline()`, `next_token` can be found with
                `response["meta"]["next_token"]`)
            - start_time (date (ISO 8601)) : The oldest or earliest UTC timestamp
                from which the Tweets will be provided. Does not override 3200 limit.
                Has second granularity, and is inclusive of that second. Minimum
                allowable time is 2010-11-06T00:00:00Z.
            - until_id (str) : Returns results with a tweet ID less less than (that
                is, older than) the specified 'until' tweet ID. Results will exclude the
                tweet ID provided. Does not override 3200 limit.

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        return self._timeline_lookup(user_id, "mentions", everything=everything, fields=fields, expansions=expansions, **kwargs)

    def _timeline_lookup(
            self,
            user_id: str,
            endpoint: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return tweets sent by (Timeline) or mentioning (Mentions) a specific user ID.
            - Max (Timeline): 3200 most recent tweets (using pagination_token)
            - Max (Mentions): 800 most recent tweets (using pagination_token)
            - Default (Both): 10 most recent tweets (tweet_id and text data fields only)
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - endpoint (str) - valid values are "followers" or "following"
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"
        
        Available kwargs:
            - See user-facing method doc-strings for available kwargs

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        # Check type of query and user_fields
        if not isinstance(user_id, str):
            raise ValueError("Invalid parameter type. `user_id` must be str")

        # Construct URL
        url = f"{self._base_url}/users/{user_id}/{endpoint}"
        # Create payload.
        payload = self._decorate_payload(
            endpoint_type='tweet',
            everything=everything,
            fields=fields,
            expansions=expansions
        )
        payload.update(kwargs)

        response = self._oauth.make_request(url, payload)
        return response.json()

    ########################################
    ########################################
    # User endpoints
    def get_followers(
            self,
            user_id: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return a list of users who are followers of the specified user ID.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"

        Available kwargs:
            - max_results (int) : The maximum number of results to be returned per page.
                This can be a number between 1 and the 1000. By default, each page will
                return 100 results.
            - pagination_token (str) : This parameter is used to move forwards or
                backwards through 'pages' of results, based on the value of the
                next_token or previous_token in the response. (E.g., after executing
                `response = get_tweet_timeline()`, `next_token` can be found with
                `response["meta"]["next_token"]`)

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        return self._follows_lookup(user_id, "followers", everything=everything, fields=fields, expansions=expansions, **kwargs)

    def get_following(
            self,
            user_id: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return a list of users the specified user ID is following.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-following

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"

        Available kwargs:
            - max_results (int) : The maximum number of results to be returned per page.
                This can be a number between 1 and the 1000. By default, each page will
                return 100 results.
            - pagination_token (str) : This parameter is used to move forwards or
                backwards through 'pages' of results, based on the value of the
                next_token or previous_token in the response. (E.g., after executing
                `response = get_tweet_timeline()`, `next_token` can be found with
                `response["meta"]["next_token"]`)

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        return self._follows_lookup(user_id, "following", everything=everything, fields=fields, expansions=expansions, **kwargs)

    def _follows_lookup(
            self,
            user_id: str,
            endpoint: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return a list of users who are followers of or followed by the specified user ID.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - endpoint (str) - valid values are "followers" or "following"
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"
        
        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        # Check type of query and user_fields
        if not isinstance(user_id, str):
            raise ValueError("Invalid parameter type. `user_id` must be str")

        # Construct URL
        url = f"{self._base_url}/users/{user_id}/{endpoint}"
        # Create payload.
        payload = self._decorate_payload(
            endpoint_type='user',
            everything=everything,
            fields=fields,
            expansions=expansions
        )
        payload.update(kwargs)

        response = self._oauth.make_request(url, payload)
        return response.json()

    def user_lookup_ids(
            self,
            user_ids: Union[list, tuple],
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None
        ) -> dict:
        """
        Looks-up user account information using unique user account id numbers.
        User fields included by default match the default parameters returned by Twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users

        Parameters:
            - user_ids (list, tuple) - unique user ids to include in query (max 100)
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - user_fields (list, tuple) - the user fields included in returned data.
            (Default = "id", "name", "username")
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        return self._user_lookup(user_ids, "id", everything=everything, fields=fields, expansions=expansions)

    def user_lookup_usernames(
            self,
            usernames: Union[list, tuple],
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None
        ) -> dict:
        """
        Looks-up user account information using account usernames.
        User fields included by default match the default parameters returned by Twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by

        Parameters:
            - usernames (list, tuple) - usernames to include in query (max 100)
            - user_fields (list, tuple) - the user fields included in returned data.
            (Default = "id", "name", "username")
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)

        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        cleaned_usernames = []
        for username in usernames:
            if username.startswith('@'):
                cleaned_usernames.append(username[1:])
            else:
                cleaned_usernames.append(username)
        return self._user_lookup(cleaned_usernames, "username", everything=everything, fields=fields, expansions=expansions)

    def _user_lookup(
            self,
            query: Union[list, tuple],
            query_type: str,
            everything: bool = False,
            fields: ObjectFields = None,
            expansions: UserExpansions = None
        ) -> dict:
        """
        Looks-up user account information using unique user id numbers.
        User fields included by default match the default parameters from twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
         and https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by

        Parameters:
            - query (list, tuple) - unique user ids or usernames (max 100)
            - query_type (str) - type of the query, can be "id" or "username"
            - everything: (bool) - if True, return all fields and expansions. (default = False)
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
        
        Returns:
            - dict

        Raises:
            - Exception
            - ValueError
        """
        query_specs = {
            "id": {
                "phrase": "user ids",
                "parameter_name": "ids",
                "endpoint": "users"
            },
            "username": {
                "phrase": "usernames",
                "parameter_name": "usernames",
                "endpoint": "users/by"
            }
        }.get(query_type)

        # Check type of query and user_fields
        if not isinstance(query, (list, tuple)):
            raise ValueError(
                "Invalid parameter type: `query` must be" "either a list or tuple."
            )

        # Make sure the query is no longer than 100
        if len(query) <= 100:
            # create payload.
            payload = {
                query_specs["parameter_name"]: f"{','.join(query)}"
            }
        else:
            raise Exception(f"You passed {len(query)} {query_specs['phrase']}. \
                This exceeds the maximum for a single query, 100")

        payload = self._decorate_payload(
            payload=payload,
            endpoint_type='user',
            everything=everything,
            fields=fields,
            expansions=expansions
        )

        # Pull Data. Wait when necessary and catching time dependent errors.
        switch = True
        url = f"{self._base_url}/{query_specs['endpoint']}"
        while switch:
            # Get response
            response = self._oauth.make_request(url, payload)

            # Get number of requests left with our tokens
            remaining_requests = int(response.headers["x-rate-limit-remaining"])

            # If that number is one, we get the reset-time
            #   and wait until then, plus 15 seconds (your welcome Twitter).
            # The regular 429 exception is caught below as well,
            #   however, we want to program defensively, where possible.
            if remaining_requests == 1:
                buffer_wait_time = 15
                resume_time = datetime.fromtimestamp( int(response.headers["x-rate-limit-reset"]) + buffer_wait_time )
                print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                pause_until(resume_time)

            # Explicitly checking for time dependent errors.
            # Most of these errors can be solved simply by waiting
            # a little while and pinging Twitter again - so that's what we do.
            if response.status_code != 200:

                # Too many requests error
                if response.status_code == 429:
                    buffer_wait_time = 15
                    resume_time = datetime.fromtimestamp( int(response.headers["x-rate-limit-reset"]) + buffer_wait_time )
                    print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                    pause_until(resume_time)

                # Twitter internal server error
                elif response.status_code == 500:
                    # Twitter needs a break, so we wait 30 seconds
                    resume_time = datetime.now().timestamp() + 30
                    print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                    pause_until(resume_time)

                # Twitter service unavailable error
                elif response.status_code == 503:
                    # Twitter needs a break, so we wait 30 seconds
                    resume_time = datetime.now().timestamp() + 30
                    print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                    pause_until(resume_time)

                # If we get this far, we've done something wrong and should exit
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )

            # Each time we get a 200 response, lets exit the function and return the response.json
            if response.ok:
                return response.json()