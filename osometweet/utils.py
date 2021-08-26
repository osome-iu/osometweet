"""
A collection of utility and convenience functions.
"""
import logging
import sys

from datetime import datetime
if sys.version_info[0] >= 3:
    from datetime import timezone

import time as pytime
from time import sleep


def get_logger(name):
    """
    Return a logging StreamHandler.

    Format : "%(asctime)s@%(name)s:%(levelname)s: %(message)s"
         - Ref: https://docs.python.org/3/howto/logging.html#formatters
    Level : "INFO"
        - Ref: https://docs.python.org/3/howto/logging.html#logging-levels

    Parameters:
    ----------
    - name (str) : the name for your logger

    """
    # Create a custom logger
    logger = logging.getLogger(name)
    # Create handlers
    handler = logging.StreamHandler()
    # Create formatters and add it to handlers
    logger_format = logging.Formatter(
        "%(asctime)s@%(name)s:%(levelname)s: %(message)s")
    handler.setFormatter(logger_format)
    # Add handlers to the logger
    logger.addHandler(handler)
    # Set level
    level = logging.getLevelName("INFO")
    logger.setLevel(level)
    return logger


def pause_until(time):
    """
    Pause your program until a specific time, specified with `time`.

    Parameters:
    ----------
    - time (datetime or unix timestamp) : pause until this time

    Exceptions:
    ----------
    - Exception
    """
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
        raise Exception(
            'The time parameter is not a number or datetime object'
        )

    # Now we wait
    while True:
        now = pytime.time()
        diff = end - now

        # Time is up!
        if diff <= 0:
            break
        else:
            # 'logarithmic' sleeping to minimize loop iterations
            sleep(diff / 2)


def chunker(seq: list, size: int) -> list:
    """
    Convert a list (seq) into a list of
    smaller lists (with len <= size), where only the
    last list will have len < size.

    Parameters:
    ----------
    - seq (list) : the iterable you'd like to chunk into
        smaller lists
    - size (int) : the size of the returned chunk(s)

    Return:
    ----------
    - list

    Exceptions:
    ----------
    - ValueError
    ~~~

    Example Usage:

    import osometweet.utils as o_utils
    my_list = [1,2,3,4,5,6,7,8,9]

    o_utils.chunker(seq = my_list, size = 2)

    # Returns
    [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
    """
    if not isinstance(seq, list):
        raise ValueError("`seq` must be a list")
    return list(seq[pos:pos + size] for pos in range(0, len(seq), size))


def convert_date_to_iso(time_string: str, time_format="%Y-%m-%d") -> str:
    """
    Convert input `time_string` to the iso format that Twitter
    requires for queries (ISO 8601/RFC 3339). Output times are
    all returned in UTC time format.

    Parameters:
    ----------
    - time_string (str): a string representation of time that should
        match the `time_format`
    - time_format (str): the datetime format code of `time_string`.
        Default `time_format` = "%Y-%m-%d", where:
            - %Y = Year with century as a decimal number (e.g. 2020)
            - %m = Month as a zero-padded decimal number (e.g. 07 for July)
            - %d = Day of the month as a zero-padded decimal number
                (e.g., 01 for the first day of the month)
            - Assumes hour, minute, and second all equal zero

    Return:
    ----------
    - str

    Exceptions:
    ----------
    - TypeError
    - ValueError
    ~~~

    Examples:
    ----------

    # Load utils
    import osometweet.utils as o_utils

    ### 1. Default usage
    o_utils.convert_date_to_iso("2020-01-01")

    # Returns
    '2020-01-01T00:00:00Z'

    ** Note that we don't specify the hour, minute,
    or seconds and the function fills in this
    information for us. **


    ### 2. Specify time format

    # Call function passing only the year
    o_utils.convert_date_to_iso(
        "2020-01-02-03-04-56",
        time_format="%Y-%m-%d-%H-%M-%S"
    )

    # Returns
    '2020-01-02T03:04:56Z'
    """
    if not isinstance(time_string, str):
        raise TypeError("`time_string` must be a string.")
    if not isinstance(time_format, str):
        raise TypeError("`time_format` must be a string.")

    try:
        date = datetime.strptime(time_string, time_format)
        date = datetime.strftime(date, "%Y-%m-%dT%H:%M:%S") + "Z"
        return date

    except ValueError:
        raise ValueError(
            f"`time_string` '{time_string}'"
            f" does not match `time_format` '{time_format}'"
        )
