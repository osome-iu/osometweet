#!/usr/bin/env python3


# Script Information
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
PURPOSE:
    - Script to scrape up to the most recent 3,200 tweets sent by a provided
    user ID by utilizing the V2 Twitter tweet timeline endpoint.

    Ref: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets

INPUT:
    - A unique user ID string.

OUTPUT:
    - timeline_data--{todays-date}.json : a file where each line
    represents one tweet for the provided user ID string.
    - timeline_errors--{todays-date}.json : a file where each line
    represents an error message returned by Twitter.

    Note: Files which are empty at the end of the data gathering process
    will be deleted (for example, if no errors are returned).

Author: Matthew R. DeVerna
"""


# Import packages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import json
from datetime import datetime as dt

import osometweet

USER_ID = "1312850357555539972"


# Create Functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_bearer_token():
    """Load Twitter Keys from Local Environment."""

    # To set your environment variables in your terminal execute a command
    # like the one that you see below.

    # Example:
    # export 'TWITTER_BEARER_TOKEN'='<your_twitter_bearer_token>'

    # Do this for all of your tokens, and then load them with the commands
    # below, matching the string in the .get("string") to the name you've
    # chosen to the left of the equal sign above.

    # Set Twitter tokens/keys.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("Loading bearer token...")
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN", None)

    if bearer_token is None:
        raise Exception(
            "No environment variable named 'TWITTER_BEARER_TOKEN'! "
            "Make sure to set this from your terminal via:\n\n"
            "\t --> 'TWITTER_BEARER_TOKEN'='<your_twitter_bearer_token>' "
        )

    return bearer_token


def initialize_osometweet(bearer_token):
    """
    Return an authorized osometweet API object
    from which we can make API calls.

    Parameters:
    ----------
    - bearer_token (str) : Your secret Twitter bearer token.
    """
    print("Initializing osometweet...")

    oauth2 = osometweet.OAuth2(
        bearer_token=bearer_token,
        manage_rate_limits=True  # Wait if Twitter sends rate limit message
    )
    return osometweet.OsomeTweet(oauth2)


def write_data(response, data_file, error_file):
    """
    Write data and/or errors to the provided file_obj.

    Parameters:
    ----------
    - response (dict) : a Twitter response from ot.get_tweet_timeline()
    - data_file (_io.TextIOWrapper) : an open data file object that you'd like
        the data from `response` to be written to
    - error_file (_io.TextIOWrapper) : an open errors file object that you'd
        like the errors from `response` to be written to
    """
    try:
        if "data" in response:
            data = response["data"]
            data_file.writelines(f"{json.dumps(line)}\n" for line in data)

        if "errors" in response:
            errors = response["errors"]
            error_file.writelines(f"{json.dumps(line)}\n" for line in errors)

    except Exception as e:
        print(e)
        raise Exception("Problem writing response info to file!")


def delete_if_empty(file_path):
    """Delete file if it's is empty"""
    if os.stat(file_path).st_size == 0:
        print(f"\t -Deleting empty file: {file_path}")
        os.remove(file_path)


def gather_data(user_id):
    """
    Gather tweets (in reverse chronological order) from the timeline of
    the user_id provided.

    Parameters:
    ----------
    - user_id (str) : the user ID whose tweets we want to download
    """

    # Load bearer token and authorize osometweet
    # to gather data...
    bearer_token = load_bearer_token()
    ot = initialize_osometweet(bearer_token)

    # Create tweet fields object with all fields
    #   NOTE: if you include other fields/expansions you will
    #   need to ensure that you parse them properly from the
    #   response object below
    all_tweet_fields = osometweet.TweetFields(everything=True)

    # Get today's date
    today = dt.strftime(dt.today(), "%Y-%m-%d_%H-%M")

    # Create file names
    data_file_name = f"timeline_data--{today}.json"
    errors_file_name = f"timeline_errors--{today}.json"

    print("Gathering data...")

    # Open a file for data and errors
    with open(data_file_name, 'w') as data_file,\
         open(errors_file_name, 'w') as error_file:

        # Make first request and write data and/or errors
        response = ot.get_tweet_timeline(
            user_id=user_id,
            fields=all_tweet_fields,  # Get all tweet fields
            max_results=100           # Request 100 tweets per call
        )
        write_data(response, data_file, error_file)

        # Begin a while loop which continually makes requests until
        # up to 3,200 tweets (or all tweets) have been returned
        # for the user_id provided. This only continues if the "next_token"
        # is present in `response["meta"]` object, which indicates that
        # Twitter has more data to provide.
        while "next_token" in response["meta"]:
            response = ot.get_tweet_timeline(
                user_id=user_id,
                fields=all_tweet_fields,
                max_results=100,
                pagination_token=response["meta"]["next_token"]
            )
            write_data(response, data_file, error_file)

    # Now that the loop has finished
    # we remove any files that might be empty
    # (for example, if we received no errors)
    delete_if_empty(data_file_name)
    delete_if_empty(errors_file_name)


# Execute the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    gather_data(user_id=USER_ID)

    print("~~~ Script Complete ~~~")
