[![PyPI version](https://badge.fury.io/py/osometweet.svg)](https://badge.fury.io/py/osometweet)

# Introduction

The OSoMeTweet project intends to provide a set of tools to help researchers work with the V2 API of Twitter.
The Wiki will work as an unofficial archive of knowledge people gather through the process.

# Contents
* [Getting Started](#getting-started)
	* [Install the PyPi version](#install-the-pypi-version)
	* [Local development](#local-development)
	* [Tests](#tests)
	* [How to seek helps and contribute](#how-to-seek-helps-and-contribute)
* [Example Usage](#example-usage)
	* [Authorization](#authentication)
		* [OAuth 1a](#oauth-1a)
		* [OAuth 2](#oauth-2)
	* [Initializing the `OsomeTweet` class](#initializing-the-osometweet-class)
	* [Pulling a User's Account Information](#pulling-a-users-account-information)
		* [Pull account information with user_id numbers - `user_lookup_ids()`](#pull-account-information-with-user_id-numbers---user_lookup_ids)
			* [Specifying `user.fields`](#specifying-userfields)
		* [Pull account information with usernames - `user_lookup_usernames()`](#pull-account-information-with-usernames---user_lookup_usernames)
	* [Utility Methods (`osometweet.utils`)](#utility-methods-osometweetutils)
		* [`o_utils.pause_until`](#o_utilspause_until)
		* [`o_utils.chunker`](#o_utilschunker)
		* [`o_utils.ObjectFields`](#o_utilsobjectfields)
	* [Pulling Followers and Following](#pulling-followers-and-following)
		* [Pull Who Follows a Specific `user_id` - `get_followers()`](#pull-who-follows-a-specific-user_id---get_followers)
		* [Pull Who a `user_id` Follows - `get_following()`](/#pull-who-a-user_id-follows---get_following)


# Getting Started
## Install the PyPi version
> [Return to top of page](#contents)
```bash
pip install osometweet
```

**Warning 1**: the package is still in development, so the functionalities are very limited and the robustness is low.

**Warning 2**: we will try to keep the interface of the package consistent, but there maybe drastic changes in the future.

## Local development

The Pypi version is behind the GitHub version.
To take advantage of the newest features and functionalities, you can install the GitHub version locally.

To do so, clone this project, go to the source directory, type the following command to install the package locally:

```bash
pip install -e .
```

## Tests

Go to `tests` directory and run:

```bash
python tests.py
```

## How to seek helps and contribute
> [Return to top of page](#contents)

OSoMeTweet will be a community project. **If you encounter bugs, please create [Issues](https://github.com/truthy/osometweet/issues)**. If you want to contribute to the project, you are welcome to create [Pull Requests](https://github.com/truthy/osometweet/pulls).

# Quick start

Here is an example of how to use our package to pull user information: 
```python
from osometweet import OsomeTweet, OAuth2

# Initialize the OSoMeTweet object
bearer_token = "YOUR_TWITTER_BEARER_TOKEN"
oauth2 = OAuth2(bearer_token=bearer_token)
ot = OsomeTweet(oauth2)

# Set some test IDs (these are Twitter's own accounts)
ids2find = ["2244994945", "6253282"]

# Call the function without these ids
response = ot.user_lookup_ids(user_ids=ids2find)
print(response["data"])
```
which returns a list of dictionaries, where each dictionary contains the requested information for an individual user.
```python
[
    {'id': '2244994945', 'name': 'Twitter Dev', 'username': 'TwitterDev'},
    {'id': '6253282', 'name': 'Twitter API', 'username': 'TwitterAPI'}
]
```

For detailed instructions, check out our [wiki](https://github.com/osome-iu/osometweet/wiki).