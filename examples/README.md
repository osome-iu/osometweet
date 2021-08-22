# Introduction

This folder is intended to house example scripts that are actually useful.

For every endpoint, we provide an example script to demonstrate how it works. Below is some high-level information about each script. However, we encourage you to examine the scripts (which are heavily commented) to better understand exactly what data they are getting from Twitter. 



| Endpoint type  | Endpoint | Note | Command |
|----------------|----------|------|---------|
| Tweet endpoint | Tweets lookup | Scrape tweets with tweet ids | `python tweet-lookup.py -f test_data/test_tweet_ids.txt` |
| User endpoint  | User lookup with ids | Scrape many users account information with ids | `python user-lookup-ids.py -f test_data/test_user_ids.txt` |
| User endpoint  | User lookup with usernames | Scrape many users account information with usernames | `python user-lookup-usernames.py -f test_data/test_user_names.txt` |
| Timeline endpoint  | Tweet timeline | Scrape a provided user ID's most recent tweets | `python tweet_timeline.py` |
| Timeline endpoint  | Mentions timeline | Scrape a provided user ID's most recent mentions | `python mentions_timeline.py` |
| Streaming endpoint  | Sample stream | Gather a real-time 1% sample of all Twitter activity | `python sampled_stream.py` |
| Streaming endpoint  | Filtered stream | Gather tweets in real-time that match the provided list of filters | `python filtered_stream.py` |