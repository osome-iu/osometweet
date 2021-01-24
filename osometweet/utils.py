""" A collection of utility and convenience functions."""


import sys
from datetime import datetime
import time as pytime
from time import sleep
if sys.version_info[0] >= 3:
    from datetime import timezone
import logging


def get_logger(name):
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