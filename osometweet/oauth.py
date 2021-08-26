"""
This module handles authorization when calling Twitter endpoints for the
`osometweet` package using both OAuth1a and OAuth2 methods.
"""
import requests
from requests_oauthlib import OAuth1Session

from osometweet.rate_limit_manager import manage_rate_limits


class OAuthHandler:
    """
    General OAuthHandler class.
    """
    def __init__(self):
        pass

    def make_request(
        self,
        method: str,
        url: str,
        payload: dict,
        stream: bool = False,
        json: dict = {}
    ) -> requests.models.Response:
        """
        Method to make the HTTP request to Twitter API

        Parameters:
        ----------
        - method (str) - HTTP request method
        - url (str) - url of the endpoint
        - payload (dict) - payload of the request
        - json (dict) - dict that will be passed to requests' json field

        Returns:
        ----------
        - requests.models.Response
        """

        # If requested, manage rate limits
        if self._manage_rate_limits:
            switch = True
            while switch:

                # Make one request
                response = self._make_one_request(
                    method, url, payload=payload, stream=stream, json=json
                )

                # The below returns:
                #    True: if there was an error that we waited for,
                #         ensuring we make the same request again
                #    False: if there were no errors, so the while-loop breaks
                switch = manage_rate_limits(response)

        else:
            # Make request
            response = self._make_one_request(
                method, url, payload=payload, stream=stream, json=json
            )

        return response


class OAuth1a(OAuthHandler):
    """
    Class to handle authentication through OAuth 1.0a with user context.

    Parameters:
    ----------
    - API key (str) : A Twitter API Key string.
    - API key secret (str) : A Twitter API Key Secret string.
        Note: Think of these as the user name and password that represents
            your Twitter developer app when making API requests.
    - Access token (str) and secret (str) : A Twitter Access Token string.
    - Access token secret (str) :  A Twitter Access Token Secret string.
    - manage_rate_limits (bool) : Whether OsomeTweet should handle potential
        rate limiting errors.
        - True (default) - Yes, manage my rate limits
        - False - No, don't manage my rate limits

    Notes:
    ----------
    - An access token and access token secret are user-specific
        credentials used to authenticate OAuth 1.0a API requests. They
        specify the Twitter account the request is made on behalf of.
    - You can pair your own Access Token and Access Token Secret strings
        with your API Key and API Key Secret strings, or you can make
        requests on behalf of another user. Follow the "Learn about OAuth
        1.0a" link below to learn more about this.
    - If you don't have an account, get access here:
        - https://developer.twitter.com/en/apply-for-access
    - Learn about OAuth 1.0a authentication here:
        - https://developer.twitter.com/en/docs/authentication/oauth-1-0a

    """

    def __init__(
        self,
        api_key: str = "",
        api_key_secret: str = "",
        access_token: str = "",
        access_token_secret: str = "",
        manage_rate_limits: bool = True,
    ) -> None:
        super(OAuth1a, self).__init__()
        self._api_key = api_key
        self._api_key_secret = api_key_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._manage_rate_limits = manage_rate_limits
        self._set_oauth_1a_creds()

    def _set_oauth_1a_creds(self) -> None:
        """
        Sets the user-based OAuth 1.0a tokens.

        Ref: https://developer.twitter.com/en/docs/authentication/oauth-1-0a

        Raises:
        ----------
        - Exception, ValueError
        """
        for key_name in [
            "api_key",
            "api_key_secret",
            "access_token",
            "access_token_secret",
        ]:
            if not isinstance(getattr(self, "_" + key_name), str):
                raise ValueError(
                    f"Invalid type for parameter {key_name}, must be a string."
                )
        # Get oauth object
        self._oauth_1a = OAuth1Session(
            self._api_key,
            client_secret=self._api_key_secret,
            resource_owner_key=self._access_token,
            resource_owner_secret=self._access_token_secret,
        )

    def _make_one_request(
        self,
        method: str,
        url: str,
        payload: dict,
        stream: bool = False,
        json: dict = {}
    ) -> requests.models.Response:
        """
        Method to make one HTTP request to Twitter API

        Parameters:
        ----------
        - method (str) - HTTP request method
        - url (str) - url of the endpoint
        - payload (dict) - payload of the request

        Returns:
        ----------
        - requests.models.Response
        """
        if method.upper() == "GET":
            response = self._oauth_1a.get(
                url,
                params=payload,
                stream=stream,
                json=json
            )
        elif method.upper() == "POST":
            response = self._oauth_1a.post(
                url,
                params=payload,
                stream=stream,
                json=json
            )
        return response


class OAuth2(OAuthHandler):
    """
    Class to handle authentication through OAuth 2.0 without user context.

    Parameters:
    ----------
    - bearer_token (str) : A bearer token associated with a Twitter developer
        account.
    - manage_rate_limits (bool) : Whether OsomeTweet should handle potential
        rate limiting errors.
        - True (default) - Yes, manage my rate limits
        - False - No, don't manage my rate limits

    Notes:
    ----------
    - OAuth 2.0 Bearer Tokens authenticate requests on behalf of your developer
        App. As this method is specific to the App, it does not involve any
        users. This method is typically for developers that need read-only
        access to public information. This authentication method requires you
        pass a Bearer Token with your request, which you can generate within
        the Keys and tokens section of your developer Apps.
    - If you don't have an account, get access here:
        - https://developer.twitter.com/en/apply-for-access
    - Learn about OAuth 2.0 here:
        - https://developer.twitter.com/en/docs/authentication/oauth-2-0

    """

    def __init__(
        self,
        bearer_token: str = "",
        manage_rate_limits: bool = True
    ) -> None:
        super(OAuth2, self).__init__()
        self._bearer_token = bearer_token
        self._manage_rate_limits = manage_rate_limits
        self._set_bearer_token()

    # Setters
    def _set_bearer_token(self) -> None:
        """
        Sets the bearer token, which authenticates the user using OAuth 2.0.

        Ref: https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens

        Raises:
        ----------
        - Exception, ValueError
        """
        if isinstance(self._bearer_token, str):
            self._header = {"Authorization": f"Bearer {self._bearer_token}"}
        else:
            raise ValueError(
                "Invalid type for parameter bearer_token, must be a string"
            )

    def _make_one_request(
        self,
        method: str,
        url: str,
        payload: dict,
        stream: bool = False,
        json: dict = {}
    ) -> requests.models.Response:
        """
        Method to make one HTTP request to Twitter API

        Parameters:
        ----------
        - method (str) - HTTP request method
        - url (str) - url of the endpoint
        - payload (dict) - payload of the request

        Returns:
        ----------
        - requests.models.Response
        """
        response = requests.request(
            method,
            url,
            headers=self._header,
            params=payload,
            stream=stream,
            json=json
        )
        return response
