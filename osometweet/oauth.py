import requests
from requests_oauthlib import OAuth1Session

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