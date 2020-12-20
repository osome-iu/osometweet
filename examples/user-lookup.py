#!/usr/bin/env python3

# Script Information
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
Purpose: Script to scrape Twitter users account information 
with the Twitters V2 user_lookup endpoint. Takes a 
file of user IDs as input.
Author: Matthew DeVerna
Date: Dec. 17th 2020
"""


# Import packages
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
import argparse
import os
from osometweet.api import OsomeTweet
from osometweet.utils import chunker
import json
from tqdm import tqdm
from datetime import datetime as dt



# Set CLI Arguments.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initiate the parser
parser = argparse.ArgumentParser(
    description="Script to scrape Twitter users account information."
)
# Add optional arguments
parser.add_argument(
    "-f", "--file",
    metavar='File',
    help="Full path to the file containing the USER IDS you would like to scrape."
)

# Read parsed arguments from the command line into "args"
args = parser.parse_args()

# Assign them to objects
file = args.file
# To set your enviornment variables in your terminal execute a command like the 
# one that you see below. Of course you can change 'CONSUMER_KEY' for whatever 
# variable you prefer
# export 'CONSUMER_KEY'='<your_bearer_token>'

# Set Twitter tokens/keys.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_key = os.environ.get("TWITTER_API_KEY")
api_key_secret = os.environ.get("TWITTER_API_KEY_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")


# Create Functions.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def chunker(seq, size):
    # A function which turns one list into a list of many lists that
    # are of length `size` or shorter (the last one)
        # This returns a list of lists
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def load_users(file):
    # Load all users, return a list of lists, each 100
    # users long.
    #   This allows us to iterate through a long list of users
    # 100 users at a time (which is the maximum number of ids
    # we can query Twitter for in one call).
    with open(file, 'r') as f:
        users = [x.strip('\n') for x in f.readlines()]

    max_query_length = 100
    chunked_user_list = chunker(
        seq = users,
        size = max_query_length
        )
    return chunked_user_list


def gather_data():
    # Initialize
    ot = OsomeTweet(
        api_key = api_key,
        api_key_secret = api_key_secret,
        access_token = access_token,
        access_token_secret = access_token_secret
        )

    # Add all user_fields
    user_fields = [
        "created_at", "description", "entities", "location",
        "pinned_tweet_id", "profile_image_url", "protected",
        "public_metrics", "url", "verified", "withheld"
    ]

    # Load the users from the file into a chunked list of
    # user id numbers. Each list's max length will be 100.
    list_of_user_lists = load_users(file)

    # Get today's date
    today = dt.strftime(dt.today(), "%Y-%m-%d_%H-%M")

    # Open two files. One for good data, the other for account errors.
    with open(f"account_data--{today}.json", 'w') as data_file, open(f"account_errors--{today}.json", 'w') as error_file:

        # Iterate through the list of lists, starting a tqdm timer
        for one_hundred_users in tqdm(list_of_user_lists):
            response = ot.user_lookup_ids(
                user_ids=one_hundred_users,
                user_fields=user_fields
            )

            # Get data and errors
            data = response["data"]
            errors = response["errors"]

            # No matter what `data` and `errors` will return, however, they may return `None`.
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
    gather_data()
    print("Data pull complete.")
