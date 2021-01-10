import requests
import pause
from typing import Union
from datetime import datetime
from requests_oauthlib import OAuth1Session
from osometweet import utils as o_util

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

        :raises ValueError
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
        
        :param str bearer_token
        :returns None
        :raises ValueError
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
                
        :param str base_url
        :returns None
        :raises ValueError
        """
        if isinstance(base_url, str):
            self._base_url = base_url
        else:
            raise ValueError("Invalid type for parameter base_url, must be a string")

    def set_expansions(self, expansions: str) -> None:
        """
        Sets the expansions that will be included in the JSON response. 
        Possible values:
            attachments.poll_ids, attachments.media_keys, author_id, entities.mentions.username,
            geo.place_id, in_reply_to_user_id, referenced_tweets.id, referenced_tweets.id.author_id
            
        Ref: https://developer.twitter.com/en/docs/twitter-api/expansions
        
        :param str expansions
        :returns None
        :raises ValueError
        """
        if isinstance(expansions, str):
            self._params["expansions"] = expansions.replace(" ", "")
        else:
            raise ValueError("Invalid type for parameter expansions, must be a string")

    # Fields
    # Ref: https://developer.twitter.com/en/docs/twitter-api/fields
    def set_media_fields(self, media_fields: str) -> None:
        """
        Sets the media fields that will be included in the JSON response. 
        Possible values:
            duration_ms, height, media_key, preview_image_url, type, url, width,
            public_metrics, non_public_metrics, organic_metrics, promoted_metrics
            
        :param str media_fields
        :returns None
        :raises ValueError
        """
        if isinstance(media_fields, str):
            self._params["media.fields"] = media_fields.replace(" ", "")
        else:
            raise ValueError(
                "Invalid type for parameter media.fields, must be a string"
            )

    def set_place_fields(self, place_fields: str) -> None:
        """
        Sets the place fields that will be included in the JSON response. 
        Possible values:
            contained_within, country, country_code, full_name, geo, id, name, place_type
      
        :param str place_fields
        :returns None
        :raises ValueError
        """
        if isinstance(place_fields, str):
            self._params["place.fields"] = place_fields.replace(" ", "")
        else:
            raise ValueError(
                "Invalid type for parameter place.fields, must be a string"
            )

    def set_poll_fields(self, poll_fields: str) -> None:
        """
        Sets the poll fields that will be included in the JSON response. 
        Possible values:
            duration_minutes, end_datetime, id, options, voting_status
            
        :param str poll_fields
        :returns None
        :raises ValueError
        """
        if isinstance(poll_fields, str):
            self._params["poll_fields"] = poll_fields.replace(" ", "")
        else:
            raise ValueError("Invalid type for parameter poll.fields, must be a string")

    def set_tweet_fields(self, tweet_fields: str) -> None:
        """
        Sets the tweet fields that will be included in the JSON response. 
        Possible values:
            attachments, author_id, context_annotations, conversation_id, created_at,
            entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, 
            public_metrics, organic_metrics, promoted_metrics, possibly_sensitive, 
            referenced_tweets, source, text, withheld
            
        :param str tweet_fields
        :returns None
        :raises ValueError
        """
        if isinstance(tweet_fields, str):
            self._params["tweet.fields"] = tweet_fields.replace(" ", "")
        else:
            raise ValueError(
                "Invalid type for parameter tweet_fields, must be a string"
            )

    def set_user_fields(self, user_fields: str) -> None:
        """
        Sets the user fields that will be included in the JSON response. 
        Possible values:
            created_at, description, entities, id, location, name, pinned_tweet_id,
            profile_image_url, protected, public_metrics, url, username, verified, withheld
            
        :param str user_fields
        :returns None
        :raises ValueError
        """
        if isinstance(user_fields, str):
            self._params["user.fields"] = user_fields.replace(" ", "")
        else:
            raise ValueError("Invalid type for parameter user_fields, must be a string")

    # Tweets
    def tweet_lookup(self, tids: Union[str, list, tuple]) -> requests.models.Response:
        """
        Looks-up at least one tweet using its tweet id.
        Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
 
        :param [str, list, tuple] tids
        :returns requests.models.Response
        :raises Exception, ValueError
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

        url = f"{self._base_url}/tweets"
        payload.update(self._params)
        response = self._oauth.make_request(url, payload)
        return response.json()

    def get_followers(
            self,
            user_id: str,
            user_fields: Union[list, tuple] = ["id", "name", "username"]
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
                url = "{}/users/{}/followers".format(self._base_url, user_id)
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
            "Invalid parameter type. Both `user_ids` and \
            `user_fields` must be either a list or tuple."
                )

        payload.update(self._params)
        response = self._oauth.make_request(url, payload)
        return response.json()

    def get_following(
            self,
            user_id: str,
            user_fields: Union[list, tuple] = ["id", "name", "username"]
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
                url = "{}/users/{}/following".format(self._base_url, user_id)
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
            "Invalid parameter type. Both `user_ids` and \
            `user_fields` must be either a list or tuple."
                )

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

        :param [list, tuple] user_ids - Unique user ids to include in query. (max 100
        :param [list, tuple] user_fields - The user fields included in returned data. 
          (Default = "id", "name", "username")

        :returns requests.models.Response

        :raises Exception, ValueError
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

        :param [list, tuple] usernames - Usernames to include in query. (max 100)
        :param [list, tuple] user_fields - The user fields included in returned data.
          (Default = "id", "name", "username")

        :returns requests.models.Response

        :raises Exception, ValueError
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
 
        :param [list, tuple] query - Unique user ids or usernames (max 100)
        :param str query_type - type of the query, can be id or username
        :returns requests.models.Response
        :raises Exception, ValueError
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