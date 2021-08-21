#!/usr/bin/env python3

# Script Information
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
PURPOSE:
    -Script to stream tweets with Twitter V2's filtered stream endpoint.
INPUT:
    - None
OUTPUT:
    - tweet_data--{todays-date}.json : a file where each line
    represents one tweet
    - tweet_errors--{todays-date}.json : a file which records any
    errors received (one per line).
Author: Christopher Torres-Lugo
"""


# Import packages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import json
from datetime import datetime as dt

import osometweet


# Create Functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_bearer_token():
    """Load Twitter Keys from Local Environment."""

    # To set your environment variables in your terminal execute a command like
    # the one that you see below.

    # Example:
    # export 'TWITTER_BEARER_TOKEN'='<your_twitter_bearer_token>'

    # Do this for all of your tokens, and then load them with the commands
    # below, matching the string in the .get("string") to the name you've
    # chosen to the left of the equal sign above.

    # Set Twitter tokens/keys.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

    return bearer_token


def stream_tweets(bearer_token):
    """
    Stream tweets from twitter and write them directly to a new line
    delimited JSON file, named with today's date in "%Y-%m-%d_%H-%M" format.

    Parameters
    ----------
    - bearer_token (str) : Twitter V2 bearer token.
    """
    print("Streaming tweets...")

    oauth2 = osometweet.OAuth2(
        bearer_token=bearer_token,
        manage_rate_limits=False
    )
    ot = osometweet.OsomeTweet(oauth2)

    # Add all tweet fields
    all_tweet_fields = osometweet.TweetFields(everything=True)

    # Add streaming rules
    rules = [{"value": "coronavirus", "tag": "all coronavirus tweets"},
             {"value": "indiana", "tag": "all indiana tweets"}]
    add_rules = {"add": rules}
    response = ot.set_filtered_stream_rule(rules=add_rules)
    print(f"API response from adding two rules: {response}")

    # Retrieve active streaming rules
    current_rules = ot.get_filtered_stream_rule()
    print(f'The current filtered stream rules are: {current_rules}')

    # Remove a streaming rule
    for data in current_rules.get('data'):
        if data['tag'] == 'all indiana tweets':
            all_indiana_tweets_id = data['id']
            break
    delete_rule = {"delete": all_indiana_tweets_id}
    ot.set_filtered_stream_rule(rules=delete_rule)

    # Get today's date
    today = dt.strftime(dt.today(), "%Y-%m-%d_%H-%M")

    # Open two files. One for good data, the other for tweet errors.
    with open(f"tweet_stream--{today}.json", "a") as data_file:
        # stream is a Generator
        stream = ot.filtered_stream(fields=all_tweet_fields)
        # We have to iterate over the stream to fetch streamed tweets
        for tweet in stream.iter_lines():
            # Get data and errors
            try:
                data = json.loads(tweet).get("data")

                # When data is found, we write it to the open file
                if data:
                    json.dump(data, data_file)
                    data_file.write("\n")
            except json.JSONDecodeError:
                pass


# Execute the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    bearer_token = load_bearer_token()
    print(bearer_token)
    if bearer_token:
        stream_tweets(bearer_token=bearer_token)
