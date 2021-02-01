#!/usr/bin/env python3

# Script Information
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
PURPOSE: 
    -Script to scrape Twitter users account information 
    with the Twitters V2 user_lookup_usernames endpoint. 

INPUT:
    - A file of usernames where each line contains one username.

OUTPUT:
    - account_data--{todays-date}.json : a file where each line
    represents one accounts information.

    - account_errors--{todays-date}.json : a file which records any
    errors received (one per line). You can then learn why certain ids
    were not returned (private, suspended, etc.).

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
    usernames_file = args.file
    return usernames_file

def load_users(usernames_file):
    # Load all users, returning a list of lists, each 100
    # users long.
    
    # This allows us to iterate through a long list of users
    # 100 users at a time (which is the maximum number of ids
    # we can query Twitter for in one call).
    with open(usernames_file, 'r') as f:
        users = [x.strip('\n') for x in f.readlines()]

    max_query_length = 100

    chunked_user_list = chunker(
        seq = users,
        size = max_query_length
        )
    return chunked_user_list

def load_keys():
    """Load Twitter Keys from Local Environment."""

    # To set your enviornment variables in your terminal execute a command like the 
    # one that you see below.

    # Example:
    # export 'TWITTER_API_KEY'='<your_twitter_api_key>'

    # Do this for all of your tokens, and then load them with the commands below,
    # matching the string in the .get("string") to the name you chosen to the
    # left of the equal sign above.

    # Set Twitter tokens/keys.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    api_key = os.environ.get("TWITTER_API_KEY")
    api_key_secret = os.environ.get("TWITTER_API_KEY_SECRET")

    return access_token, access_token_secret, api_key, api_key_secret

def gather_data(
    access_token,
    access_token_secret,
    api_key,
    api_key_secret,
    chunked_user_list,
    usernames_file
    ):
    print("Gathering Data...")

    oauth1a = osometweet.OAuth1a(
        api_key = api_key,
        api_key_secret = api_key_secret,
        access_token = access_token,
        access_token_secret = access_token_secret
        )
    ot = osometweet.OsomeTweet(oauth1a)

    # Add all user_fields
    all_user_fields = osometweet.UserFields(everything = True)

    # Get today's date
    today = dt.strftime(dt.today(), "%Y-%m-%d_%H-%M")

    # Open two files. One for good data, the other for account errors.
    with open(f"account_data--{today}.json", 'w') as data_file, open(f"account_errors--{today}.json", 'w') as error_file:

        # Iterate through the list of lists
        for one_hundred_users in chunked_user_list:
            response = ot.user_lookup_usernames(
                usernames=one_hundred_users,
                fields=all_user_fields
            )

            # Where as the user_ids endpoint always returns both "data" and
            # "errors", the username endpoint does the opposite - only including
            # these keys if data is present.
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
    usernames_file = parse_cl_args()
    chunked_user_list = load_users(usernames_file)
    access_token, access_token_secret, api_key, api_key_secret = load_keys()
    
    gather_data(
        access_token = access_token,
        access_token_secret = access_token_secret,
        api_key = api_key,
        api_key_secret = api_key_secret,
        chunked_user_list = chunked_user_list,
        usernames_file = usernames_file,
    )

    print("Data pull complete.")
