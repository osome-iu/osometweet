[![PyPI version](https://badge.fury.io/py/osometweet.svg)](https://badge.fury.io/py/osometweet)
[![v2](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2)](https://developer.twitter.com/en/docs/twitter-api)

### Introduction

The OSoMeTweet project intends to provide a set of tools to help researchers work with Twitter's V2 API.

The [Wiki](https://github.com/osome-iu/osometweet/wiki) includes a detailed documentation of how to use all methods. Also, we will use the wiki to store knowledge gathered by those who are building this package.

- [Install](#installation)
- [Quick Start](#quick-start)
- [Learn how to use the package](#learn-how-to-use-the-package)
- [Learn about Twitter V2](#learn-about-twitter-v2) 
- [Example scipts](#example-scripts) 
- [Wiki](https://github.com/osome-iu/osometweet/wiki)

### Installation
#### Install the PyPI version
```bash
pip install osometweet
```

**Warning 1**: The package is still in development, so not all endpoints are included and those which are included may not be 100% robust. Please see the list of issues for known problems. 

**Warning 2**: We will try to keep the interface of the package consistent, but there may be drastic changes in the future.

#### Use the newest features & local development

The PyPI version may be behind the GitHub version.
To ensure that you are using the latest features and functionalities, you can install the GitHub version locally.

To do so, clone this project, go to the source directory, and run `pip install -e .` 

If you want to do this with `git` it should look something like the below, run from your command line:

```bash
git clone https://github.com/osome-iu/osometweet.git
cd ./osometweet
pip install -e .
```

#### Requirements

```bash
python>=3.5
requests>=2.24.0
requests_oauthlib>=1.3.0
```

#### Tests

Go to `tests` directory and run:

```bash
python tests.py
```

> Note: you will need to have the following environment variables set in order for the tests to
work properly.
> - TWITTER_API_KEY
> - TWITTER_API_KEY_SECRET
> - TWITTER_ACCESS_TOKEN
> - TWITTER_ACCESS_TOKEN_SECRET
> - TWITTER_BEARER_TOKEN
> 
> If you're not sure what these are, check out [this](https://developer.twitter.com/en/docs/authentication/overview) page to learn how Twitter authentication works.

### How to seek help and contribute

OSoMeTweet will be a community project and your help is welcome!

See [How to contribute to the OsoMeTweet package](https://github.com/osome-iu/osometweet/blob/master/CONTRIBUTING.md) for more details on how to contribute.

### Quick start

Here is an example of how to use our package to pull user information: 
```python
import osometweet

# Initialize the OSoMeTweet object
bearer_token = "YOUR_TWITTER_BEARER_TOKEN"
oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
ot = osometweet.OsomeTweet(oauth2)

# Set some test IDs (these are Twitter's own accounts)
ids2find = ["2244994945", "6253282"]

# Call the function with these ids as input
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

### Learn how to use the package
Documentation on how to use all package methods are located in the [Wiki](https://github.com/osome-iu/osometweet/wiki). 

**Start here before using the [example scripts](#examples)!**

### Learn about Twitter V2
We have documented (and will continue to document) information about Twitter's V2 API that we deem is valuable. For example:
* [Details on Twitter's new fields/expansions parameters](https://github.com/osome-iu/osometweet/wiki/Info:-Available-Fields-and-Expansions)
* [Available Endpoints](https://github.com/osome-iu/osometweet/wiki/Info:-Available-Twitter-API-V2-Endpoints)
* [HTTP Status Codes and Errors](https://github.com/osome-iu/osometweet/wiki/Info:-HTTP-Status-Codes-and-Errors)
* Academic Track [Benefits](https://github.com/osome-iu/osometweet/wiki/Info:-Academic-Track-Benefits) and [Details](https://github.com/osome-iu/osometweet/wiki/Info:-Academic-Track-Details)

### Example Scripts
We offer [example scripts](examples) for working with different endpoints. We recommend that you read and understand the methods by reading the relevant package [Wiki](https://github.com/osome-iu/osometweet/wiki) pages prior to using these scripts.
