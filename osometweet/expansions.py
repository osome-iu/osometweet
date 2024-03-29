"""
This module contains classes for handling the available User and Tweet
expansion fields.
"""

from typing import Union
from osometweet.utils import get_logger

logger = get_logger(__name__)


class ObjectExpansions:
    """
    General Twitter expansions class.
    """
    avail_expansions = []
    def __init__(self):
        self._expansions = self.avail_expansions

    @property
    def expansions(self):
        return self._expansions

    @expansions.setter
    def expansions(self, value: Union[list, tuple]):
        if not isinstance(value, (list, tuple)):
            raise ValueError(
                "Invalid parameter type."
                "`expansions` must be a list or tuple."
            )
        avail_expansions = set(self.avail_expansions)
        new_expansions = set(value)
        valid_new_expansions = list(avail_expansions & new_expansions)
        invalid_new_expansions = list(
            new_expansions - (avail_expansions & new_expansions)
        )
        if invalid_new_expansions:
            logger.warning(
                f"{invalid_new_expansions} are not "
                "valid expansions and ignored."
            )
        self._expansions = valid_new_expansions

    @property
    def expansions_object(self):
        return {"expansions": ",".join(self._expansions)}

    def __repr__(self):
        return ",".join(self.expansions)


class TweetExpansions(ObjectExpansions):
    """
    Tweet Expansions class. Expansion classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available tweet expansions

    import osometweet.expansions as o_expansions
    expansions = o_expansions.TweetExpansions()
    print(expansions.avail_expansions)


    # 2. Specify specific tweet expansions

    import osometweet.expansions as o_expansions
    expansions = o_expansions.TweetExpansions()
    expansions.expansions = ["author_id"]

    """
    avail_expansions = [
        "attachments.poll_ids", "attachments.media_keys", "author_id",
        "entities.mentions.username", "geo.place_id", "in_reply_to_user_id",
        "referenced_tweets.id", "referenced_tweets.id.author_id"
    ]

    def __init__(self):
        super(TweetExpansions, self).__init__()


class UserExpansions(ObjectExpansions):
    """
    User Expansions class. Expansion classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available user expansions

    import osometweet.expansions as o_expansions
    expansions = o_expansions.UserExpansions()
    print(expansions.avail_expansions)


    # 2. Specify specific user expansions

    import osometweet.expansions as o_expansions
    expansions = o_expansions.UserExpansions()
    expansions.expansions = ["pinned_tweet_id"]

    """
    avail_expansions = ["pinned_tweet_id"]
    def __init__(self):
        super(UserExpansions, self).__init__()
