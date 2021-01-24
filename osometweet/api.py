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

    ########################################
    # Tweet endpoints
    def tweet_lookup(
            self,
            tids: Union[str, list, tuple],
            fields: ObjectFields = None,
            expansions: TweetExpansions = None
        ) -> dict:
        """
        Looks-up at least one tweet using its tweet id.
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets

        Parameters:
            - tids: (str, list, tuple) - Up to 100 unique tweet ids.
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (TweetExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
        Returns:
            dict
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
        # Include expansions if present
        if expansions is not None and isinstance(expansions, TweetExpansions):
            payload.update(expansions.expansions_object)
        # Include fields if present
        if fields is not None:
            payload.update(fields.fields_object)
        response = self._oauth.make_request(url, payload)
        return response.json()

    ########################################
    # User endpoints
    def get_followers(
            self,
            user_id: str,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return a list of users who are followers of the specified user ID.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"
        Returns:
            dict
        Raises:
            - Exception
            - ValueError
        """
        return self._follows_lookup(user_id, "followers", fields=fields, expansions=expansions, **kwargs)

    def get_following(
            self,
            user_id: str,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return a list of users the specified user ID is following.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-following

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"
        Returns:
            dict
        Raises:
            - Exception
            - ValueError
        """
        return self._follows_lookup(user_id, "following", fields=fields, expansions=expansions, **kwargs)

    def _follows_lookup(
            self,
            user_id: str,
            endpoint: str,
            fields: ObjectFields = None,
            expansions: UserExpansions = None,
            **kwargs
        ) -> dict:
        """
        Return a list of users who are followers of or followed by the specified user ID.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - endpoint (str) - valid values are "followers" or "following"
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
            - kwargs - for optional arguments like "max_results" and "pagination_token"
        Returns:
            dict
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
        payload = dict()
        payload.update(kwargs)
        # Include expansions if present
        if expansions is not None and isinstance(expansions, UserExpansions):
            payload.update(expansions.expansions_object)
        # Include fields if present
        if fields is not None:
            payload.update(fields.fields_object)

        response = self._oauth.make_request(url, payload)
        return response.json()

    def user_lookup_ids(
            self,
            user_ids: Union[list, tuple],
            fields: ObjectFields = None,
            expansions: UserExpansions = None
        ) -> dict:
        """
        Looks-up user account information using unique user account id numbers.
        User fields included by default match the default parameters returned by Twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users

        Parameters:
            - user_ids (list, tuple) - unique user ids to include in query (max 100)
            - user_fields (list, tuple) - the user fields included in returned data.
            (Default = "id", "name", "username")
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
        Returns:
            - dict
        Raises:
            - Exception, ValueError
        """
        return self._user_lookup(user_ids, "id", fields=fields, expansions=expansions)

    def user_lookup_usernames(
            self,
            usernames: Union[list, tuple],
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
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
        Returns:
            - dict
        Raises:
            - Exception, ValueError
        """
        cleaned_usernames = []
        for username in usernames:
            if username.startswith('@'):
                cleaned_usernames.append(username[1:])
            else:
                cleaned_usernames.append(username)
        return self._user_lookup(cleaned_usernames, "username", fields=fields, expansions=expansions)

    def _user_lookup(
            self,
            query: Union[list, tuple],
            query_type: str,
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
            - fields: (ObjectFields) - additional fields to return. (default = None)
            - expansions: (UserExpansions) - Expansions enable requests to
            expand an ID into a full object in the response. (default = None)
        Returns:
            - dict
        Raises:
            - Exception, ValueError
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

        if expansions is not None and isinstance(expansions, UserExpansions):
            payload.update(expansions.expansions_object)
        # Include fields if present
        if fields is not None:
            payload.update(fields.fields_object)

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