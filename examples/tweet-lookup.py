#!/usr/bin/env python3

# Script Information
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
PURPOSE:
    - Script to scrape tweets with the Twitter V2 get tweets endpoint

INPUT:
    - A file of tweet IDs where each line contains one id

OUTPUT:
    - tweet_data--{todays-date}.json : a file where each line
    represents one tweet

    - tweet_errors--{todays-date}.json : a file which records any
    errors received (one per line). You can then learn why certain ids
    were not returned.

Author: Matthew R. DeVerna, Kaicheng Yang
"""


# Import packages
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import argparse
import os
import json
from datetime import datetime as dt

import osometweet
from osometweet.utils import chunker

# Create Functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_cl_args():
    """Set CLI Arguments."""

    # Initiate the parser
    parser = argparse.ArgumentParser(
        description="Script to scrape tweet information."
    )
    # Add optional arguments
    parser.add_argument(
        "-f", "--file",
        metavar='File',
        help="Full path to the file containing the "
        "USER IDS you would like to scrape.",
        required=True
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    # Assign the file name to a variable and return it
    ids_file = args.file
    return ids_file

def load_tweet_ids(ids_file):
    """
    Load all tweet ids, returning a list of lists, each 100
    users long.
    """

    with open(ids_file, 'r') as f:
        tweet_ids = [x.strip('\n') for x in f.readlines()]

    max_query_length = 100

    # This allows us to iterate through a long list of tweet ids
    # 100 tweets at a time (which is the maximum number of ids
    # we can query Twitter for in one call).
    chunked_list = chunker(
        seq=tweet_ids,
        size=max_query_length
        )
    return chunked_list

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
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

    return bearer_token

def gather_data(
        bearer_token,
        chunked_list
    ):
    """
    Gather tweets based on the chunked list of tweet IDs with the provided
    bearer_token.
    """
    print("Gathering Data...")

    oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
    ot = osometweet.OsomeTweet(oauth2)

    # Add all tweet fields
    all_tweet_fields = osometweet.TweetFields(everything=True)

    # Get today's date
    today = dt.strftime(dt.today(), "%Y-%m-%d_%H-%M")

    # Open two files. One for good data, the other for tweet errors.
    with open(f"tweet_data--{today}.json", 'w') as data_file,\
         open(f"tweet_errors--{today}.json", 'w') as error_file:

        # Iterate through the list of lists
        for one_hundred_tweets in chunked_list:
            response = ot.tweet_lookup(
                tids=one_hundred_tweets,
                fields=all_tweet_fields
            )

            # Get data and errors
            data = response["data"]
            errors = response["errors"]

            # No matter what `data` and `errors` will return something,
            # however, they may return `None` (i.e. no data/errors), which
            # will throw a TypeError.
            try:
                data_file.writelines(f"{json.dumps(line)}\n" for line in data)
            except TypeError:
                print(
                    "No data found in this set of tweets, "
                    "skipping to the next set."
                )

            try:
                error_file.writelines(
                    f"{json.dumps(line)}\n" for line in errors
                )
            except TypeError:
                print(
                    "No problematic tweets found in this set of tweets, "
                    "skipping to the next set."
                )


# Execute the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    ids_file = parse_cl_args()
    chunked_list = load_tweet_ids(ids_file)
    bearer_token = load_bearer_token()

    gather_data(
        bearer_token=bearer_token,
        chunked_list=chunked_list
    )

    print("Data pull complete.")
