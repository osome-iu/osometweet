""" A collection of utility and convenience functions."""


import sys
from datetime import datetime
import time as pytime
from time import sleep
if sys.version_info[0] >= 3:
    from datetime import timezone


def pause_until(time):
    """ Pause your program until a specific end time. 'time' is either
    a valid datetime object or unix timestamp in seconds (i.e. seconds
    since Unix epoch) """
    end = time

    # Convert datetime to unix timestamp and adjust for locality
    if isinstance(time, datetime):
        # If we're on Python 3 and the user specified a timezone, 
        # convert to UTC and get tje timestamp.
        if sys.version_info[0] >= 3 and time.tzinfo:
            end = time.astimezone(timezone.utc).timestamp()
        else:
            zoneDiff = pytime.time() - (datetime.now() - datetime(1970, 1, 1)).total_seconds()
            end = (time - datetime(1970, 1, 1)).total_seconds() + zoneDiff

    # Type check
    if not isinstance(end, (int, float)):
        raise Exception('The time parameter is not a number or datetime object')

    # Now we wait
    while True:
        now = pytime.time()
        diff = end - now

        #
        # Time is up!
        #
        if diff <= 0:
            break
        else:
            # 'logarithmic' sleeping to minimize loop iterations
            sleep(diff / 2)


def chunker(seq: list, size: int) -> list:
    """ Turns a list (seq) into a list of
    smaller lists len <= size, where only the
    last list will have len < size.

    :param iterable seq
    :param int size

    return list
    ~~~

    Example Usage:

        import osometweet.utils as o_utils
    my_list = [1,2,3,4,5,6,7,8,9]
    o_utils.chunker(seq = my_list, size = 2)
    [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
    """
    if isinstance(seq, list) == False:
        raise ValueError("`seq` must be a list")
    return list(seq[pos:pos + size] for pos in range(0, len(seq), size))


class ObjectFields():
    """ Class of convenience methods for Twitter's object fields.
    """

    # Show Fields
    # ~~~~~~~~~~~~~~~
    def show_user_fields():
        """ Show all possible twitter v2 user fields.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.show_user_fields()
        """
        fields = [
            "Twitter V2 Available User Fields:",
            "created_at",
            "description",
            "entities",
            "id",
            "location",
            "name",
            "pinned_tweet_id",
            "profile_image_url",
            "protected",
            "public_metrics",
            "url",
            "username",
            "verified",
            "withheld",
            "Reference: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user"
        ]
        print(*fields, sep="\n-")

    def show_tweet_fields():
        """ Show all possible twitter v2 user fields.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.show_tweet_fields()
        """
        fields = [
            "Twitter V2 Available Tweet Fields:",
            "attachments",
            "author_id",
            "context_annotations",
            "conversation_id",
            "created_at",
            "entities",
            "geo",
            "id",
            "in_reply_to_user_id",
            "lang",
            "non_public_metrics",
            "organic_metrics",
            "possiby_sensitive",
            "promoted_metrics",
            "public_metrics",
            "referenced_tweets",
            "reply_settings",
            "source",
            "text",
            "withheld",
            "Reference: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet"
        ]
        print(*fields, sep="\n-")

    def show_media_fields():
        """ Show all possible twitter v2 user fields.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.show_media_fields()
        """
        fields = [
            "Twitter V2 Available Media Fields:",
            "duration_ms",
            "height",
            "media_key",
            "non_public_metrics",
            "organic_metrics",
            "preview_image_url",
            "promoted_metrics",
            "public_metrics",
            "type",
            "width",
            "Reference: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media"
        ]
        print(*fields, sep="\n-")

    def show_poll_fields():
        """ Show all possible twitter v2 poll fields.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.show_poll_fields()
        """
        fields = [
            "Twitter V2 Available Poll Fields:",
            "duration_minutes",
            "end_datetime",
            "id",
            "options",
            "voting_status",
            "Reference: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/poll"
        ]
        print(*fields, sep="\n-")

    def show_place_fields():
        """ Show all possible twitter v2 poll fields.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.show_place_fields()
        """
        fields = [
            "Twitter V2 Available Place Fields:",
            "contained_within",
            "country",
            "country_code",
            "full_name",
            "geo",
            "id",
            "name",
            "place_type",
            "Reference: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place"
        ]
        print(*fields, sep="\n-")

    # Return Fields
    # ~~~~~~~~~~~~~~~
    def return_user_fields():
        """ Return all possible twitter v2 user fields as a list.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.return_user_fields()

        """
        fields = [
            "created_at",
            "description",
            "entities",
            "id",
            "location",
            "name",
            "pinned_tweet_id",
            "profile_image_url",
            "protected",
            "public_metrics",
            "url",
            "username",
            "verified",
            "withheld"
        ]
        return fields

    def return_tweet_fields():
        """ Return all possible twitter v2 tweet fields as a list.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.return_tweet_fields()
        """
        fields = [
            "attachments",
            "author_id",
            "context_annotations",
            "conversation_id",
            "created_at",
            "entities",
            "geo",
            "id",
            "in_reply_to_user_id",
            "lang",
            "non_public_metrics",
            "organic_metrics",
            "possiby_sensitive",
            "promoted_metrics",
            "public_metrics",
            "referenced_tweets",
            "reply_settings",
            "source",
            "text",
            "withheld"
        ]
        return fields

    def return_media_fields():
        """ Return all possible twitter v2 media fields as a list.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.return_media_fields()
        """
        fields = [
            "duration_ms",
            "height",
            "media_key",
            "non_public_metrics",
            "organic_metrics",
            "preview_image_url",
            "promoted_metrics",
            "public_metrics",
            "type",
            "width"
        ]
        return fields

    def return_poll_fields():
        """ Return all possible twitter v2 poll fields as a list.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.return_poll_fields()
        """
        fields = [
            "duration_minutes",
            "end_datetime",
            "id",
            "options",
            "voting_status"
        ]
        return fields

    def return_place_fields():
        """ Return all possible twitter v2 place fields as a list.
        ~~~

        Example Usage:

        from osometweet.utils import ObjectFields as fields
        fields.return_place_fields()
        """
        fields = [
            "contained_within",
            "country",
            "country_code",
            "full_name",
            "geo",
            "id",
            "name",
            "place_type",
        ]
        return fields
