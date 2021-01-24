from typing import Union
from osometweet.utils import get_logger

logger = get_logger(__name__)


class ObjectFields:
    def __init__(self, fields_object=None):
        self._fields_object = {} if fields_object is None else fields_object

    @property
    def fields_object(self):
        return self._fields_object

    def __add__(self, value: "ObjectFields"):
        if isinstance(value, ObjectFields):
            return ObjectFields(fields_object={**self.fields_object, **value.fields_object})
        else:
            return self

    def __radd__(self, value: "ObjectFields"):
        return self.__add__(value)

    def __repr__(self):
        return str(self.fields_object)


class ObjectFieldsBase(ObjectFields):
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
        if not isinstance(value, (list,tuple)):
            raise ValueError(
                    "Invalid parameter type."
                    "`fields` must be a list or tuple."
                )
        avail_fields = set(self.default_fields + self.optional_fields)
        new_fields = set(value)
        valid_new_fields = list(avail_fields & new_fields)
        invalid_new_fields = list(new_fields - (avail_fields & new_fields))
        if invalid_new_fields:
            logger.warning(f"{invalid_new_fields} are not valid fields and ignored.")
        self._fields = valid_new_fields

    @property
    def fields_object(self):
        return {self.parameter_name: ",".join(self._fields)}

    def __repr__(self):
        return ",".join(self.fields)


class UserFields(ObjectFieldsBase):
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
    default_fields = ["id", "options"]
    optional_fields = ["duration_minutes", "end_datetime", "voting_status"]
    parameter_name = "poll.fields"
    def __init__(self, everything: bool = False):
        super(PollFields, self).__init__(everything=everything)


class PlaceFields(ObjectFieldsBase):
    default_fields = ["full_name", "id"]
    optional_fields = [
        "contained_within", "country", "country_code",
        "geo", "name", "place_type"
    ]
    parameter_name = "place.fields"
    def __init__(self, everything: bool = False):
        super(PlaceFields, self).__init__(everything=everything)


def get_all_avail_fields() -> "ObjectFields":
    return sum([
        TweetFields(everything=True),
        UserFields(everything=True),
        MediaFields(everything=True),
        PollFields(everything=True),
        PlaceFields(everything=True)
    ])