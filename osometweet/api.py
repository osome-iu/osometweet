import requests
import pause
from typing import Union
from datetime import datetime
from requests_oauthlib import OAuth1Session
import osometweet.utils as o_util

o_fields = o_util.ObjectFields

class OAuthHandler:
    def __init__(self):
        pass

    def make_request(self):
        pass


class OAuth1a(OAuthHandler):
    def __init__(
        self,
        api_key: str = "",
        api_key_secret: str = "",
        access_token: str = "",
        access_token_secret = "",

    ) -> None:
        self._api_key = api_key
        self._api_key_secret = api_key_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._set_oauth_1a_creds()

    def _set_oauth_1a_creds(self) -> None:
        """
        Sets the user-based OAuth 1.0a tokens.
        Ref: https://developer.twitter.com/en/docs/authentication/oauth-1-0a

        Raises:
            - Exception, ValueError
        """
        for key_name in ['api_key', 'api_key_secret', 'access_token', 'access_token_secret']:
            if not isinstance(getattr(self, '_' + key_name), str):
                raise ValueError(
                    f"Invalid type for parameter {key_name}, must be a string."
                    )
        # Get oauth object
        self._oauth_1a = OAuth1Session(
            self._api_key,
            client_secret = self._api_key_secret,
            resource_owner_key = self._access_token,
            resource_owner_secret = self._access_token_secret
            )

    def make_request(
        self,
        url: str,
        payload: dict
       ) -> requests.models.Response:
        """
        Method to make the http request to Twitter API

        Parameters:
            - url (str) - url of the endpoint
            - payload (dict) - payload of the request
        Returns:
            - requests.models.Response
        """
        return self._oauth_1a.get(url, params=payload)


class OAuth2(OAuthHandler):
    """
    Class to handle authenticiation through OAuth 2.0 without user context
    Only bearer token is required for this class
    """
    def __init__(
        self,
        bearer_token: str= "",
    ) -> None:
        self._bearer_token = bearer_token
        self._set_bearer_token()
    
    # Setters
    def _set_bearer_token(self) -> None:
        """
        Sets the bearer token, which authenticates the user using OAuth 2.0.
        Ref: https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens
        
        Raises: 
            - Exception, ValueError
        """
        if isinstance(self._bearer_token, str):
            self._header = {"Authorization": f"Bearer {self._bearer_token}"}
        else:
            raise ValueError(
                "Invalid type for parameter bearer_token, must be a string"
            )

    def make_request(
        self,
        url: str,
        payload: dict
    ) -> requests.models.Response:
        """
        Method to make the http request to Twitter API

        Parameters:
            - url (str) - url of the endpoint
            - payload (dict) - payload of the request
        Returns:
            - requests.models.Response
        """
        return requests.get(
            url,
            headers=self._header,
            params=payload
        )


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
            
    # Tweets
    def tweet_lookup(
            self,
            tids: Union[str, list, tuple],
            expansions: Union[list, tuple] = None,
            media_fields: Union[list, tuple] = None,
            place_fields: Union[list, tuple] = None,
            poll_fields: Union[list, tuple] = None,
            tweet_fields: Union[list, tuple] = None,
            user_fields: Union[list, tuple] = None
        ) -> requests.models.Response:
        """
        Looks-up at least one tweet using its tweet id.
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
 
        Parameters:
            - tids: (str, list, tuple) - Up to 100 unique tweet ids.
            - expansions: (list, tuple) - Expansions enable requests to
            expand an ID into a full object in the includes response
            object. (default = None)
            - media_fields: (list, tuple) - additional fields to return
            in the media object. The response will contain the selected
            fields only if a Tweet contains media attachments.(default = None)
            - place_fields: (list, tuple) - additional fields to return
            in the place object. The response will contain the selected
            fields only if location data is present in any of the response
            objects.(default = None)
            - poll_fields: (list, tuple) - additional fields to return
            in the poll object. The response will contain the selected
            fields only if a Tweet contains a poll.(default = None)
            - tweet_fields: (list, tuple) - additional fields to return
            in the Tweet object. By default, `tweet_lookup` enters a
            value of None which returns the `id` and `text` fields.
            - user_fields: (list, tuple) - additional fields to return
            in the user object. User field objects not returned unless
            explicitly included. (default = None)
        Returns:
            requests.models.Response
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

        # Include expansions if present
        if expansions is not None:
            if isinstance(expansions, (list,tuple)):
                avail_expansions = [
                "attachments.poll_ids", "attachments.media_keys", "author_id", 
                "entities.mentions.username", "geo.place_id", "in_reply_to_user_id",
                 "referenced_tweets.id", "referenced_tweets.id.author_id"
                 ]
                if all([x in avail_expansions for x in expansions]):
                    if len(expansions) == 1:
                        self._params.update({
                            "expansions" : expansions[0]
                            })
                    else:
                        self._params.update({
                            "expansions" : ",".join(expansions)
                            })
                else:
                    raise Exception(
                        "One or more of the passed expansions are not valid.\
                        Use osometweet.utils.ObjectFields methods to check options."
                        )
            else:
                raise ValueError(
                        "Invalid parameter type. `expansions` must be a\
                        list or tuple."
                    )

        # Include media fields if present
        if media_fields is not None:
            if isinstance(media_fields, (list,tuple)):
                avail_media_fields = o_fields.return_media_fields()
                if all([x in avail_media_fields for x in media_fields]):
                    if len(media_fields) == 1:
                        self._params.update({
                            "media.fields" : media_fields[0]
                            })
                    else:
                        self._params.update({
                            "media.fields" : ",".join(media_fields)
                            })
                else:
                    raise Exception(
                        "One or more of the passed media fields are not valid.\
                        Use osometweet.utils.ObjectFields methods to check options."
                        )
            else:
                raise ValueError(
                        "Invalid parameter type. `media_fields` must be a\
                        list or tuple."
                    )

        # Include place fields if present
        if place_fields is not None:
            if isinstance(place_fields, (list,tuple)):
                avail_place_fields = o_fields.return_place_fields()
                if all([x in avail_place_fields for x in place_fields]):
                    if len(place_fields) == 1:
                        self._params.update({
                            "place.fields" : place_fields[0]
                            })
                    else:
                        self._params.update({
                            "place.fields" : ",".join(place_fields)
                            })
                else:
                    raise Exception(
                        "One or more of the passed place fields are not valid.\
                        Use osometweet.utils.ObjectFields methods to check options."
                        )
            else:
                raise ValueError(
                        "Invalid parameter type. `place_fields` must be a\
                        list or tuple."
                    )

        # Include poll fields if present
        if poll_fields is not None:
            if isinstance(poll_fields, (list,tuple)):
                avail_poll_fields = o_fields.return_poll_fields()
                if all([x in avail_poll_fields for x in poll_fields]):
                    if len(poll_fields) == 1:
                        self._params.update({
                            "poll.fields" : poll_fields[0]
                            })
                    else:
                        self._params.update({
                            "poll.fields" : ",".join(poll_fields)
                            })
                else:
                    raise Exception(
                        "One or more of the passed poll fields are not valid.\
                        Use osometweet.utils.ObjectFields methods to check options."
                        )
            else:
                raise ValueError(
                        "Invalid parameter type. `poll_fields` must be a\
                        list or tuple."
                    )

        # Include tweet fields if present
        if tweet_fields is not None:
            if isinstance(tweet_fields, (list,tuple)):
                avail_tweet_fields = o_fields.return_tweet_fields()
                if all([x in avail_tweet_fields for x in tweet_fields]):
                    if len(tweet_fields) == 1:
                        self._params.update({
                            "tweet.fields" : tweet_fields[0]
                            })
                    else:
                        self._params.update({
                            "tweet.fields" : ",".join(tweet_fields)
                            })
                else:
                    raise Exception(
                        "One or more of the passed tweet fields are not valid.\
                        Use osometweet.utils.ObjectFields methods to check options."
                        )
            else:
                raise ValueError(
                        "Invalid parameter type. `tweet_fields` must be a\
                        list or tuple."
                    )

        # Include user fields if present
        if user_fields is not None:
            if isinstance(tweet_fields, (list,tuple)):
                if "author_id" in expansions:
                    avail_user_fields = o_fields.return_user_fields()
                    if all([x in avail_user_fields for x in user_fields]):
                        if len(user_fields) == 1:
                            self._params.update({
                                "user.fields" : user_fields[0]
                                })
                        else:
                            self._params.update({
                                "user.fields" : ",".join(user_fields)
                                })
                    else:
                        raise Exception(
                            "One or more of the passed user_fields are not valid.\
                            Use osometweet.utils.ObjectFields methods to check options."
                            )
                else:
                    raise Exception(
                        "`author_id` missing from `expansions`.\
                        `To use the `user_fields` parameter, you must also\
                        include the `author_id` expansion parameter in\
                        your request.")
            else:
                raise ValueError(
                        "Invalid parameter type. `tweet_fields` must be a\
                        list or tuple."
                    )

        # Set url and update payload with params
        url = f"{self._base_url}/tweets"
        payload.update(self._params)
        response = self._oauth.make_request(url, payload)
        return response.json()

    def get_followers(
            self,
            user_id: str,
            user_fields: Union[list, tuple] = ["id", "name", "username"],
            **kwargs
        ) -> requests.models.Response:
        """
        Return a list of users who are followers of the specified user ID.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - user_fields (list, tuple) - The user fields included in returned data.
            (Default = "id", "name", "username")
            - kwargs - for optional arguments like "max_results" and "pagination_token"

        Returns:
            requests.models.Response

        Raises:
            - Exception
            - ValueError
        """
        return self._follows_lookup(user_id, "followers", user_fields, **kwargs)

    def get_following(
            self,
            user_id: str,
            user_fields: Union[list, tuple] = ["id", "name", "username"],
            **kwargs
        ) -> requests.models.Response:
        """
        Return a list of users the specified user ID is following.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-following

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - user_fields (list, tuple) - The user fields included in returned data.
            (Default = "id", "name", "username")
            - kwargs - for optional arguments like "max_results" and "pagination_token"

        Returns:
            requests.models.Response

        Raises:
            - Exception
            - ValueError
        """
        return self._follows_lookup(user_id, "following", user_fields, **kwargs)

    def _follows_lookup(
            self,
            user_id: str,
            endpoint: str,
            user_fields: Union[list, tuple] = ["id", "name", "username"],
            **kwargs
        ) -> requests.models.Response:
        """
        Return a list of users who are followers of or followed by the specified user ID.
            - Max: 1000 user objects per query
            - Default: 100 user objects per query
        https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

        Parameters:
            - user_id (str) - Unique user ID to include in the query
            - user_fields (list, tuple) - The user fields included in returned data.
            (Default = "id", "name", "username")
            - endpoint (str) - valid values are "followers" or "following"
            - kwargs - for optional arguments like "max_results" and "pagination_token"

        Returns:
            requests.models.Response

        Raises:
            - Exception
            - ValueError
        """

        available_user_fields = [
            "created_at", "description", "entities", "id",
            "location", "name", "pinned_tweet_id", "profile_image_url",
            "protected", "public_metrics", "url", "username", "verified", "withheld"
        ]

        # Check type of query and user_fields
        if (isinstance(user_id, str)) and (isinstance(user_fields, (list,tuple))):
            # Check all provided user fields are in the available set
            if all([x in available_user_fields for x in user_fields]):
                # Insert user_ids into urls
                url = f"{self._base_url}/users/{user_id}/{endpoint}"
                # Update payload.
                payload = {
                "user.fields": f"{','.join(user_fields)}"
                }

            else:
                raise Exception(
                    f"Invalid user_field(s) provided. Please make sure \
                    they are one of the following fields:\n\n \
                    {print(x) for x in available_user_fields}")
        else:
            raise ValueError(
            "Invalid parameter type. `user_id` must be str and \
            `user_fields` must be either a list or tuple."
                )
        payload.update(kwargs)
        payload.update(self._params)
        response = self._oauth.make_request(url, payload)
        return response.json()

    # User-Lookup
    def user_lookup_ids(
            self,
            user_ids: Union[list, tuple],
            user_fields: Union[list, tuple] = ["id", "name", "username"]
        ) -> dict:
        """
        Looks-up user account information using unique user account id numbers.
        User fields included by default match the default parameters returned by Twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users

        Parameters:
            - user_ids (list, tuple) - unique user ids to include in query (max 100)
            - user_fields (list, tuple) - the user fields included in returned data. 
            (Default = "id", "name", "username")
        Returns:
            - requests.models.Response
        Raises:
            - Exception, ValueError
        """
        return self._user_lookup(user_ids, "id", user_fields=user_fields)

    def user_lookup_usernames(
            self,
            usernames: Union[list, tuple],
            user_fields: Union[list, tuple] = ["id", "name", "username"]
        ) -> dict:
        """
        Looks-up user account information using account usernames.
        User fields included by default match the default parameters returned by Twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by

        Parameters:
            - usernames (list, tuple) - usernames to include in query (max 100)
            - user_fields (list, tuple) - the user fields included in returned data. 
            (Default = "id", "name", "username")
        Returns:
            - requests.models.Response
        Raises:
            - Exception, ValueError
        """
        cleaned_usernames = []
        for username in usernames:
            if username.startswith('@'):
                cleaned_usernames.append(username[1:])
            else:
                cleaned_usernames.append(username)
        return self._user_lookup(cleaned_usernames, "username", user_fields=user_fields)

    def _user_lookup(
            self, 
            query: Union[list, tuple], 
            query_type: str,
            user_fields: Union[list, tuple] = ["id", "name", "username"]
        ) -> dict:
        """
        Looks-up user account information using unique user id numbers. 
        User fields included by default match the default parameters from twitter.
        Ref: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
         and https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by
 
        Parameters:
            - query (list, tuple) - unique user ids or usernames (max 100)
            - query_type (str) - type of the query, can be "id" or "username"
        Returns:
            - requests.models.Response
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

        available_user_fields = [
            "created_at", "description", "entities", "id", 
            "location", "name", "pinned_tweet_id", "profile_image_url", 
            "protected", "public_metrics", "url", "username", "verified", "withheld"
        ]

        # Check type of query and user_fields 
        if (isinstance(query, (list, tuple))) and (isinstance(user_fields, (list,tuple))):
            # Check all provided user fields are in the available set
            if all([x in available_user_fields for x in user_fields]):
                # Check no more than 100 ids were passed
                if len(query) <= 100:
                    # Update payload.
                    payload = {
                    query_specs["parameter_name"]: f"{','.join(query)}",
                    "user.fields": f"{','.join(user_fields)}"
                    }

                else:
                    raise Exception(f"You passed {len(query)} {query_specs['phrase']}. \
                        This exceeds the maximum for a single query, 100")

            else:
                raise Exception(
                    f"Invalid user_field(s) provided. Please make sure \
                    they are one of the following fields:\n\n \
                    {print(x) for x in available_user_fields}")
        else:
            raise ValueError(
            "Invalid parameter type. Both `query` and \
            `user_fields` must be either a list or tuple."
                )

        # Update payload with any preset parameters
        # building on top of what may have already been set with 
        # set_user_fields()
        payload.update(self._params)

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
                o_util.pause_until(resume_time)

            # Explicitly checking for time dependent errors.
            # Most of these errors can be solved simply by waiting
            # a little while and pinging Twitter again - so that's what we do.
            if response.status_code != 200:

                # Too many requests error
                if response.status_code == 429:
                    buffer_wait_time = 15 
                    resume_time = datetime.fromtimestamp( int(response.headers["x-rate-limit-reset"]) + buffer_wait_time )
                    print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                    o_util.pause_until(resume_time)

                # Twitter internal server error
                elif response.status_code == 500:
                    # Twitter needs a break, so we wait 30 seconds
                    resume_time = datetime.now().timestamp() + 30
                    print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                    o_util.pause_until(resume_time)

                # Twitter service unavailable error
                elif response.status_code == 503:
                    # Twitter needs a break, so we wait 30 seconds
                    resume_time = datetime.now().timestamp() + 30
                    print(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
                    o_util.pause_until(resume_time)

                # If we get this far, we've done something wrong and should exit
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )
            
            # Each time we get a 200 response, lets exit the function and return the response.json
            if response.ok:
                return response.json()