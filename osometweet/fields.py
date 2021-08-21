"""
This module contains classes for handling the available Twitter
data object fields.
"""

from typing import Union
from osometweet.utils import get_logger

logger = get_logger(__name__)


class ObjectFields:
    """
    General Twitter data object fields class.
    """
    def __init__(self, fields_object=None):
        self._fields_object = {} if fields_object is None else fields_object

    @property
    def fields_object(self):
        return self._fields_object

    def __add__(self, value: "ObjectFields"):
        if isinstance(value, ObjectFields):
            return ObjectFields(
                fields_object={**self.fields_object, **value.fields_object}
            )
        else:
            return self

    def __radd__(self, value: "ObjectFields"):
        return self.__add__(value)

    def __repr__(self):
        return str(self.fields_object)


class ObjectFieldsBase(ObjectFields):
    """
    General Twitter data object fields class base.
    """
    default_fields = []
    optional_fields = []
    parameter_name = ""

    def __init__(self, everything: bool = False):
        self.everything = everything
        if self.everything:
            self._fields = self.default_fields + self.optional_fields
        else:
            self._fields = self.default_fields

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value: Union[list, tuple]):
        if not isinstance(value, (list, tuple)):
            raise ValueError(
                "Invalid parameter type."
                "`fields` must be a list or tuple."
            )
        avail_fields = set(self.default_fields + self.optional_fields)
        new_fields = set(value)
        valid_new_fields = list(avail_fields & new_fields)
        invalid_new_fields = list(new_fields - (avail_fields & new_fields))
        if invalid_new_fields:
            logger.warning(
                f"{invalid_new_fields} are not valid fields and ignored."
            )
        self._fields = valid_new_fields

    @property
    def fields_object(self):
        return {self.parameter_name: ",".join(self._fields)}

    def __repr__(self):
        return ",".join(self.fields)


class UserFields(ObjectFieldsBase):
    """
    User Fields class. Fields classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available user fields

    import osometweet.fields as o_fields
    user_fields = o_fields.UserFields()
    print(user_fields.default_fields)
    print(user_fields.optional_fields)


    # 2. Specify specific user fields

    import osometweet.fields as o_fields
    user_fields = o_fields.UserFields()
    user_fields.fields = ['id', 'name', 'created_at', 'description']


    # 3. Check which fields are currently in your user fields class

    import osometweet.fields as o_fields
    user_fields = o_fields.UserFields()
    user_fields.fields = ['id', 'name', 'created_at', 'description']
    print(user_fields.fields)

    # 4. Combining fields objects

    NOTE: The below is an example which will work interchangeably
        for all different types of fields objects, not just the below

    import osometweet.fields as o_fields
    # Intialize fields objects
    tweet_fields = o_fields.TweetFields()
    user_fields = o_fields.UserFields()

    # Manually set them
    tweet_fields.fields = ['public_metrics', 'created_at']
    user_fields.fields = ['created_at']

    sum_of_fields = tweet_fields + user_fields
    # OR
    sum_of_fields = sum([tweet_fields, user_fields])

    # Which will create the below (print(sum_of_fields) to see) which can
    # be passed directly to any of the methods fields arguments.
    {'tweet.fields': 'created_at,public_metrics', 'user.fields': 'created_at'}
    """
    default_fields = ["id", "name", "username"]
    optional_fields = [
        "created_at", "description", "entities", "location",
        "pinned_tweet_id", "profile_image_url", "protected",
        "public_metrics", "url", "verified", "withheld"
    ]
    parameter_name = "user.fields"

    def __init__(self, everything: bool = False):
        super(UserFields, self).__init__(everything=everything)


class TweetFields(ObjectFieldsBase):
    """
    Tweet Fields class. Fields classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available tweet fields

    import osometweet.fields as o_fields
    tweet_fields = o_fields.TweetFields()
    print(tweet_fields.default_fields)
    print(tweet_fields.optional_fields)


    # 2. Specify specific tweet fields

    import osometweet.fields as o_fields
    tweet_fields = o_fields.TweetFields()
    tweet_fields.fields = ['id', 'public_metrics', 'created_at']


    # 3. Check which fields are currently in your tweet fields class

    import osometweet.fields as o_fields
    tweet_fields = o_fields.TweetFields()
    tweet_fields.fields = ['id', 'public_metrics', 'created_at']
    print(tweet_fields.fields)


    # 4. Combining fields objects

    NOTE: The below is an example which will work interchangeably
        for all different types of fields objects, not just the below

    import osometweet.fields as o_fields
    # Intialize fields objects
    tweet_fields = o_fields.TweetFields()
    user_fields = o_fields.UserFields()

    # Manually set them
    tweet_fields.fields = ['public_metrics', 'created_at']
    user_fields.fields = ['created_at']

    sum_of_fields = tweet_fields + user_fields
    # OR
    sum_of_fields = sum([tweet_fields, user_fields])

    # Which will create the below (print(sum_of_fields) to see) which can
    # be passed directly to any of the methods fields arguments.
    {'tweet.fields': 'created_at,public_metrics', 'user.fields': 'created_at'}
    """
    default_fields = ["id", "text"]
    optional_fields = [
        "attachments", "author_id", "context_annotations",
        "conversation_id", "created_at", "entities", "geo",
        "in_reply_to_user_id", "lang", "possibly_sensitive",
        "public_metrics", "referenced_tweets", "reply_settings",
        "source", "withheld"
    ]
    # Extra fields only available to the owner of the account
    extra_fields = [
        "non_public_metrics", "organic_metrics", "promoted_metrics"
    ]
    parameter_name = "tweet.fields"

    def __init__(self, everything: bool = False):
        super(TweetFields, self).__init__(everything=everything)


class MediaFields(ObjectFieldsBase):
    """
    Media Fields class. Fields classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available media fields

    import osometweet.fields as o_fields
    media_fields = o_fields.MediaFields()
    print(media_fields.default_fields)
    print(media_fields.optional_fields)


    # 2. Specify specific media fields

    import osometweet.fields as o_fields
    media_fields = o_fields.MediaFields()
    media_fields.fields = ['media_key', 'duration_ms', 'height']


    # 3. Check which fields are currently in your media fields class

    import osometweet.fields as o_fields
    media_fields = o_fields.MediaFields()
    media_fields.fields = ['media_key', 'duration_ms', 'height']
    print(media_fields.fields)


    # 4. Combining fields objects

    NOTE: The below is an example which will work interchangeably
        for all different types of fields objects, not just the below

    import osometweet.fields as o_fields
    # Intialize fields objects
    tweet_fields = o_fields.TweetFields()
    user_fields = o_fields.UserFields()

    # Manually set them
    tweet_fields.fields = ['public_metrics', 'created_at']
    user_fields.fields = ['created_at']

    sum_of_fields = tweet_fields + user_fields
    # OR
    sum_of_fields = sum([tweet_fields, user_fields])

    # Which will create the below (print(sum_of_fields) to see) which can
    # be passed directly to any of the methods fields arguments.
    {'tweet.fields': 'created_at,public_metrics', 'user.fields': 'created_at'}
    """
    default_fields = ["media_key", "type"]
    optional_fields = [
        "duration_ms", "height", "preview_image_url",
        "public_metrics", "width"
    ]
    # Extra fields only available to the owner of the account
    extra_fields = [
        "non_public_metrics", "organic_metrics", "promoted_metrics"
    ]
    parameter_name = "media.fields"

    def __init__(self, everything: bool = False):
        super(MediaFields, self).__init__(everything=everything)


class PollFields(ObjectFieldsBase):
    """
    Poll Fields class. Fields classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available poll fields

    import osometweet.fields as o_fields
    poll_fields = o_fields.PollFields()
    print(poll_fields.default_fields)
    print(poll_fields.optional_fields)


    # 2. Specify specific poll fields

    import osometweet.fields as o_fields
    poll_fields = o_fields.PollFields()
    poll_fields.fields = ['options', 'duration_minutes', 'end_datetime']


    # 3. Check which fields are currently in your poll fields class

    import osometweet.fields as o_fields
    poll_fields = o_fields.PollFields()
    poll_fields.fields = ['options', 'duration_minutes', 'end_datetime']
    print(poll_fields.fields)


    # 4. Combining fields objects

    NOTE: The below is an example which will work interchangeably
        for all different types of fields objects, not just the below

    import osometweet.fields as o_fields
    # Intialize fields objects
    tweet_fields = o_fields.TweetFields()
    user_fields = o_fields.UserFields()

    # Manually set them
    tweet_fields.fields = ['public_metrics', 'created_at']
    user_fields.fields = ['created_at']

    sum_of_fields = tweet_fields + user_fields
    # OR
    sum_of_fields = sum([tweet_fields, user_fields])

    # Which will create the below (print(sum_of_fields) to see) which can
    # be passed directly to any of the methods fields arguments.
    {'tweet.fields': 'created_at,public_metrics', 'user.fields': 'created_at'}
    """
    default_fields = ["id", "options"]
    optional_fields = ["duration_minutes", "end_datetime", "voting_status"]
    parameter_name = "poll.fields"

    def __init__(self, everything: bool = False):
        super(PollFields, self).__init__(everything=everything)


class PlaceFields(ObjectFieldsBase):
    """
    Place Fields class. Fields classes can be provided
    as input to API methods.

    How to use:
    ----------

    # 1. Return all available place fields

    import osometweet.fields as o_fields
    place_fields = o_fields.PlaceFields()
    print(place_fields.default_fields)
    print(place_fields.optional_fields)


    # 2. Specify specific place fields

    import osometweet.fields as o_fields
    place_fields = o_fields.PlaceFields()
    place_fields.fields = ['full_name', 'contained_within', 'country']


    # 3. Check which fields are currently in your place fields class

    import osometweet.fields as o_fields
    place_fields = o_fields.PlaceFields()
    place_fields.fields = ['full_name', 'contained_within', 'country']
    print(place_fields.fields)


    # 4. Combining fields objects

    NOTE: The below is an example which will work interchangeably
        for all different types of fields objects, not just the below

    import osometweet.fields as o_fields
    # Intialize fields objects
    tweet_fields = o_fields.TweetFields()
    user_fields = o_fields.UserFields()

    # Manually set them
    tweet_fields.fields = ['public_metrics', 'created_at']
    user_fields.fields = ['created_at']

    sum_of_fields = tweet_fields + user_fields
    # OR
    sum_of_fields = sum([tweet_fields, user_fields])

    # Which will create the below (print(sum_of_fields) to see) which can
    # be passed directly to any of the methods fields arguments.
    {'tweet.fields': 'created_at,public_metrics', 'user.fields': 'created_at'}
    """
    default_fields = ["full_name", "id"]
    optional_fields = [
        "contained_within", "country", "country_code",
        "geo", "name", "place_type"
    ]
    parameter_name = "place.fields"

    def __init__(self, everything: bool = False):
        super(PlaceFields, self).__init__(everything=everything)
