# Introduction

This folder is intended to house example scripts that are actually useful.

# Tweet endpoints

## Tweets lookup with ids

`tweet-lookup.py` is command-line script for scraping many tweets. It takes

```bash
python tweet-lookup.py -f test_data/test_tweet_ids.txt
```

# User endpoints

## User lookup with ids

* `user-lookup-ids.py` : A command-line script for scraping many users account information. This script takes a file containing user IDs on each line as an input. You can test this script with the file [`test_data/test_user_ids.txt`](https://github.com/truthy/osometweet/blob/master/examples/test_data/test_user_ids.txt) which is a random collection of user IDs, one per row. If you'd like to use this script on a different set of user IDs, the input file of new user IDs must follow the same format.

## User lookup with usernames

* `user-lookup-usernames.py` : A command-line script for scraping many users account information. This script takes a file containing usernames on each line as an input. You can test this script with the file [`test_data/test_user_names.txt`](https://github.com/osome-iu/osometweet/blob/documentation/examples/test_data/test_user_names.txt) which is a random collection of usernames, one per row. If you'd like to use this script on a different set of usernames, the input file of new usernames must follow the same format.