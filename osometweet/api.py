import requests
from typing import Union


class OsomeTweet:
    def __init__(
        self,
        bearer_token: str = "",
        base_url: str = "https://api.twitter.com/2",
    ) -> None:
        self._bearer_token = bearer_token
        self._base_url = base_url
        self._bearer_token = bearer_token
        self._header = {"Authorization": f"Bearer {self._bearer_token}"}
        self._params = {
            "expansions": "",
            "media.fields": "",
            "place.fields": "",
            "poll.fields": "",
            "tweet.fields": "",
            "user.fields": "",
        }

    # Setters
    def set_bearer_token(self, bearer_token: str) -> None:
        """
        Sets the bearer token, which authenticates the user using OAuth 2.0.
        Ref: https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens
        
        :param str bearer_token
        :returns None
        :raises ValueError
        """
        if isinstance(bearer_token, str):
            self._bearer_token = bearer_token
            self._header = {"Authorization": f"Bearer {self._bearer_token}"}
        else:
            raise ValueError(
                "Invalid type for parameter bearer_token, must be a string"
            )

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

    # API methods
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
            params = {"ids": tids}
        elif isinstance(tids, (list, tuple)):
            if len(tids) > 100:
                raise Exception("Number of tweet ids exceeds maximum of 100")
            payload = {"ids": ",".join(tids)}
        else:
            raise ValueError(
                "Invalid type for parameter 'tids', must be a string, list, or tuple"
            )

        payload.update(self._params)
        return requests.get(
            f"{self._base_url}/tweets", headers=self._header, params=payload
        )