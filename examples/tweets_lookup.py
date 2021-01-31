#!/usr/bin/env python3

# Script Information
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
PURPOSE: 
    - Script to hydrate (gather data on) tweet IDs 

INPUT:
    - A file of tweet IDs where each line contains one user_id

OUTPUT:
    - tweet_data--{todays-date}.json : a file where each line
    represents one tweet's information.

    - tweet_errors--{todays-date}.json : a file which records any
    errors received (one per line). You can then learn why certain tweets
    were not returned.

Author: Matthew R. DeVerna
"""


# Import packages
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
import argparse
import os
import osometweet
from osometweet.utils import chunker
import json
from datetime import datetime as dt

# Create Functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_cl_args():
    """Set CLI Arguments."""

    # Initiate the parser
    parser = argparse.ArgumentParser(
        description="Script to scrape Twitter users account information."
    )
    # Add optional arguments
    parser.add_argument(
        "-f", "--file",
        metavar='File',
        help="Full path to the file containing the USER IDS you would like to scrape.",
        required=True
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    # Assign the file name to a variable and return it
    ids_file = args.file
    return ids_file

def load_tweet_ids(ids_file):
    # Load all tweet IDs, returning a list of lists, each 100
    # users long.
    
    # This allows us to iterate through a long list of tweets
    # 100 tweets at a time (which is the maximum number of tweets
    # we can query Twitter for in one call).

    with open(ids_file, 'r') as f:
        users = [x.strip('\n') for x in f.readlines()]

    max_query_length = 100

    chunked_tweets_list = chunker(
        seq = users,
        size = max_query_length
        )
    return chunked_tweets_list

def load_bearer_token():
    """Load Twitter Keys from Local Environment."""

    # To set your enviornment variables in your terminal execute a command like the 
    # one that you see below.

    # Example:
    # export 'TWITTER_BEARER_TOKEN'='<your_twitter_bearer_token>'

    # Do this for all of your tokens, and then load them with the commands below,
    # matching the string in the .get("string") to the name you chosen to the
    # left of the equal sign above.

    # Set Twitter tokens/keys.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

    return bearer_token

def gather_data(
    bearer_token,
    chunked_tweets_list,
    tweets_file
    ):
    print("Gathering Data...")

    oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
    ot = osometweet.OsomeTweet(oauth2)

    # Get today's date
    today = dt.strftime(dt.today(), "%Y-%m-%d_%H-%M")

    # Open two files. One for good data, the other for account errors.
    with open(f"tweet_data--{today}.json", 'w') as data_file, open(f"tweet_errors--{today}.json", 'w') as error_file:

        # Iterate through the list of lists
        for one_hundred_tweets in chunked_tweets_list:
            response = ot.tweet_lookup(
                tids=one_hundred_tweets,
                everything=True             # Include all tweet fields and expansions
            )

            # Grab the data/errors of each response,
            # set to None if nothing returned
            if "data" in response:
                data = response["data"]
            else:
                data = None

            if "errors" in response:
                errors = response["errors"]
            else:
                errors = None

            try:
                data_file.writelines(f"{json.dumps(line)}\n" for line in data)
            except TypeError:
                print(
                    "No USER data found in this set of users, skipping to the next set.")
                pass

            try:
                error_file.writelines(f"{json.dumps(line)}\n" for line in errors)
            except TypeError:
                print(
                    "No problematic users found in this set of user, skipping to the next set.")
                pass

# Exectue the program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    ids_file = parse_cl_args()
    chunked_tweets_list = load_tweet_ids(ids_file)
    bearer_token = load_bearer_token()
    
    gather_data(
        bearer_token = bearer_token,
        chunked_tweets_list = chunked_tweets_list,
        tweets_file = ids_file,
    )

    print("Data pull complete.")