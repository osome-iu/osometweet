[![PyPI version](https://badge.fury.io/py/osometweet.svg)](https://badge.fury.io/py/osometweet)

# Introduction

The OSoMeTweet project intends to provide a set of tools to help the researchers work with the V2 API of Twitter.
The Wiki will work as an unofficial archive of knowledge people gather through the process.

# Contents
* [Getting Started](#getting-started)
	* [Install the PyPi version](#install-the-pypi-version)
	* [Local development](#local-development)
	* [Tests](#tests)
	* [How to seek helps and contribute](#how-to-seek-helps-and-contribute)
* [Example Usage](#example-usage)
	* [Initializing the `OsomeTweet` class](#initializing-the-osometweet-class)
		* [Controlling which authorization type you'd like to use](#controlling-which-authorization-type-youd-like-to-use)
	* [Pulling a User's Account Information](#pulling-a-users-account-information)
		* [Pull account information with user_id numbers - `user_lookup_ids()`](#pull-account-information-with-user_id-numbers---user_lookup_ids)
			* [Specifying `user.fields`](#specifying-userfields)
		* [Pull account information with usernames - `user_lookup_usernames()`](#pull-account-information-with-usernames---user_lookup_usernames)
	* [Utility Methods (`osometweet.utils`)](#utility-methods-osometweetutils)
		* [`o_utils.pause_until`](#o_utilspause_until)
		* [`o_utils.chunker`](#o_utilschunker)
		* [`o_utils.ObjectFields`](#o_utilsobjectfields)


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

# Example Usage

## Initializing the `OsomeTweet` class
> [Return to top of page](#contents)

Before making use of `osometweet` to gather data, you must first initialize the `OsomeTweet` class. When initializing the `OsomeTweet` class, you must also provide `osometweet` your Twitter credentials in order to access Twitter's data. See below for an example:

```python
from osometweet.api import OsomeTweet

api_key = "YOUR_TWITTER_API_KEY"
api_key_secret = "YOUR_TWITTER_API_KEY_SECRET"
access_token = "YOUR_TWITTER_ACCESS_TOKEN"
access_token_secret = "YOUR_TWITTER_ACCESS_TOKEN_SECRET"
bearer_token = "YOUR_TWITTER_BEARER_TOKEN"

ot = OsomeTweet(
	api_key = api_key,
	api_key_secret = api_key_secret,
	access_token = access_token,
	access_token_secret = access_token_secret,
	bearer_token = bearer_token
	)
```
**Hint:** You can set your Twitter credentials in your terminal by using the `export` command like so...
```bash
export 'TWITTER_API_KEY'='YOUR_TWITTER_API_KEY'
export 'TWITTER_API_KEY_SECRET'='YOUR_TWITTER_API_KEY_SECRET'
...
```
You can do this for all of your keys/tokens and then import them to your Python environment by using the `os` package in the following way.
```python
api_key = os.environ.get("TWITTER_API_KEY")
api_key_secret = os.environ.get("TWITTER_API_KEY_SECRET")
...
```
This is valuable because you can then leave your keys/tokens - which should always be kept private - out of your code. This allows you to write code which is easier to share with others.
> **NOTE:** There are two different types of Oauth methods. [OAuth 1.0a](https://developer.twitter.com/en/docs/authentication/oauth-1-0a) (User Context) and [OAuth 2.0 Bearer Token](https://developer.twitter.com/en/docs/authentication/oauth-2-0) (App Context). **`osometweet` utilizes the OAuth 2.0 Bearer Token by default. This matters because, for certain endpoints, how many requests you can make during a given period of time changes based on which type of authorization you are using**. The best place to see these comparisons is under the _Migrate_ pages for a given endpoint in Twitter's documentation. Here is an example for the [User Lookup endpoints](https://developer.twitter.com/en/docs/twitter-api/users/lookup/migrate).

### Controlling which authorization type you'd like to use
As mentioned above, `osometweet` defaults to OAuth 2.0 Bearer Token authorization. If you'd like to use OAuth 1.0a authorization you can do that in two ways. 

1. **Don't provide the `OsomeTweet` class your `bearer_token`** 
    * `osometweet` needs your `bearer_token` for OAuth 2.0 Bearer Token authorization. Thus, if you do not provide this token, `osometweet` will look for your `bearer_token` - not find it - and then only use your user context Twitter keys/tokens (i.e. `api_key`, `api_key_secret`, `access_token`, `access_token_secret`) from then on. For example, simply initialize the `OsomeTweet` class like this...
```python
from osometweet.api import OsomeTweet

api_key = "YOUR_TWITTER_API_KEY"
api_key_secret = "YOUR_TWITTER_API_KEY_SECRET"
access_token = "YOUR_TWITTER_ACCESS_TOKEN"
access_token_secret = "YOUR_TWITTER_ACCESS_TOKEN_SECRET"

ot = OsomeTweet(
	api_key = api_key,
	api_key_secret = api_key_secret,
	access_token = access_token,
	access_token_secret = access_token_secret
	)
```

2. **Manually**
	* Perhaps you have a more complicated script and you'd like to switch which authorization `osometweet` uses for different methods. You can manually do this by controlling what `osometweet` does with `OsomeTweet._use_bearer_token` (boolean). For example:
```python
from osometweet.api import OsomeTweet

api_key = "YOUR_TWITTER_API_KEY"
api_key_secret = "YOUR_TWITTER_API_KEY_SECRET"
access_token = "YOUR_TWITTER_ACCESS_TOKEN"
access_token_secret = "YOUR_TWITTER_ACCESS_TOKEN_SECRET"
bearer_token = "YOUR_TWITTER_BEARER_TOKEN"

ot = OsomeTweet(
	api_key = api_key,
	api_key_secret = api_key_secret,
	access_token = access_token,
	access_token_secret = access_token_secret,
	bearer_token = bearer_token
	)

# The below line tells osometweet to NOT use the bearer_token even though it has been provided
ot._use_bearer_token = False  # <-------

# You can then switch it back with...
ot._use_bearer_token = True
```
> **WARNING**: `OsomeTweet._use_bearer_token` can only be set to the boolean values `True` or `False` - any other value will break the class.

## Pulling a User's Account Information
> [Return to top of page](#contents)

Account information can be gathered with two different types of queries:
1. Query **using user ID numbers**  - this is the `id` parameter within `the user.fields` object
2. Query **using the account's `username`**
    * More details on the user object model and `user.fields` parameters can be found [here](https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user).
> **Note**: A user can change their `username` but they can't change their `user_id` number. As a result, it is recommended that you gather data using `user_id` numbers because they are more reliable.

**We can query Twitter with up to 100 user IDs or usernames per query. Here's what it looks like to pull two user IDs with the `.user_lookup_ids()` method, which requires we pass it a `list` (or `tuple`) of account user IDs.**



### Pull account information with `user_id` numbers - `user_lookup_ids()`
```python
from osometweet.api import OsomeTweet

# !!! We use the user context authorization method here because
# !!! we can make more requests that way.
api_key = "YOUR_TWITTER_API_KEY"
api_key_secret = "YOUR_TWITTER_API_KEY_SECRET"
access_token = "YOUR_TWITTER_ACCESS_TOKEN"
access_token_secret = "YOUR_TWITTER_ACCESS_TOKEN_SECRET"

ot = OsomeTweet(
	api_key = api_key,
	api_key_secret = api_key_secret,
	access_token = access_token,
	access_token_secret = access_token_secret
	)

# Set some test IDs (these are Twitter's own accounts)
ids2find = ["2244994945", "6253282"]

# Call the function without these ids
response = ot.user_lookup_ids(user_ids=ids2find)
print(response["data"])
```
which returns a list of dictionaries, where each dictionary contains the requested information for an individual user.
```python
[{'id': '2244994945', 'name': 'Twitter Dev', 'username': 'TwitterDev'},
 {'id': '6253282', 'name': 'Twitter API', 'username': 'TwitterAPI'}]
```

#### Specifying `user.fields`
As you can see, the default parameters included are `id`, `name`, and `username`. However, you can request whatever parameters you want by passing a list into the `user_fields` parameters. So, after initializing the `OsomeTweet` with your Twitter tokens/keys, you can do the following:
```python
# Set some test IDs (these are Twitter's own accounts)
ids2find = ["2244994945", "6253282"]
my_fields = ["created_at", "description"]

# Call the function without these ids
response = ot.user_lookup_ids(user_ids=ids2find, user_fields=my_fields)
print(response["data"])
```
which returns a list of dictionaries, like before, but this time with the fields we requested (as well as the default `name`, `id`, and `username` fields)
```python
[{'created_at': '2013-12-14T04:35:55.000Z',
  'id': '2244994945',
  'description': 'The voice of the #TwitterDev team and your official source for updates, news, and events, related to the #TwitterAPI.',
  'name': 'Twitter Dev',
  'username': 'TwitterDev'},
 {'created_at': '2007-05-23T06:01:13.000Z',
  'id': '6253282',
  'description': 'Tweets about changes and service issues. Follow @TwitterDev\xa0for more.',
  'name': 'Twitter API',
  'username': 'TwitterAPI'}]
```



### Pull account information with `username`s - `user_lookup_usernames()`
The process for pulling account information using an account's user names is exactly the same as using `user_id`s except we now use the `user_lookup_usernames()` method and provide usernames. So, **after initializing the `OsomeTweet` with your Twitter tokens/keys**, you can do the following:
```python

# Set some test IDs (these are Twitter's own accounts)
usernames2find = ["TwitterDev", "TwitterAPI"]
my_fields = ["created_at", "description","id"]

# Call the function without these ids
response = ot.user_lookup_usernames(usernames=usernames2find, user_fields=my_fields)
print(response["data"])
```
which returns a list of dictionaries, like before, but this time with the fields we requested
```python
[{'name': 'Twitter Dev',
  'description': 'The voice of the #TwitterDev team and your official source for updates, news, and events, related to the #TwitterAPI.',
  'username': 'TwitterDev',
  'created_at': '2013-12-14T04:35:55.000Z',
  'id': '2244994945'},
 {'name': 'Twitter API',
  'description': 'Tweets about changes and service issues. Follow @TwitterDev\xa0for more.',
  'username': 'TwitterAPI',
  'created_at': '2007-05-23T06:01:13.000Z',
  'id': '6253282'}]
```

## Utility Methods (`osometweet.utils`)
> [Return to top of page](#contents)

We also include a few utility methods which will (hopefully) make working with the new Twitter API structure a bit more useful.

First, you can import the utility methods into your environment with the following code...

```python
import osometweet.utils as o_utils
```
... which will allow you to work with the `o_utils` object to access the methods.

#### `o_utils.pause_until`
Managing time is an important aspect of gathering data from Twitter and often you'd just like to wait some specified time. This is relatively easy with the `time` module, however, it is even easier with the `pause_until()` method. Simply input the time that you would like to pause your code until, and the method handles the rest. This method can take in a `datetime` object or a Unix epoch time-stamp. For example, if you'd like to wait ten seconds, you can simple do...
```python
import osometweet.utils as o_utils
import datetime as datetime

# The below line of code takes the time at the current moment, converts it to an epoch time-stamp
# and then adds ten seconds to it.
now_plus_10_with_epoch_timestamp = datetime.datetime.now().timestamp() + 10

# Then we input that into the pause_until() method and your machine will
# sleep until that specific time, ten seconds later
o_utils.pause_until(now_plus_10_with_epoch_timestamp)
```
If you'd like to do this with a `datetime`object, it looks like this...
```python
import osometweet.utils as o_utils
import datetime as datetime

# The timedelta method takes input in the following way...
# timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
now_plus_10_with_datetime_object = datetime.datetime.now() + datetime.timedelta(seconds=10)
o_utils.pause_until(now_plus_10_with_datetime_object)
```

#### `o_utils.chunker`
Another reality of working with Twitter data is that you are only allowed to query Twitter with a maximum number of users/tweets/whatever per endpoint. To deal with this, we created the `o_utils.chunker` method which turns a list into a list of smaller lists where the length of those smaller lists are no longer than the user indicated size. For example...
```python
from osometweet import utils as o_util
my_list = ["user1","user2","user3","user4","user5","user6","user7","user8","user9"]
chunked_list = o_util.chunker(seq = my_list, size = 2)
print(chunked_list)
```
which returns...
```python
[['user1', 'user2'], ['user3', 'user4'], ['user5', 'user6'], ['user7', 'user8'], ['user9']]
```

#### `o_utils.ObjectFields`
Within the `osometweet.utils` file there is a class called `ObjectFields` which contains a number of simple, yet, useful methods. Within this class there are *two types of methods:*
1. `return_object_fields`: methods to **return** a list of the available Twitter object fields
2. `show_object_fields`: methods to **print** a list of the available Twitter object fields as well as a link to a reference page on developer.twitter.com.

> **NOTE**: Methods exists for each object model (tweets, users, etc.)

The full list these methods are as follows:

Return Methods:
* `return_media_fields` - return a list of all **media** object fields.
* `return_place_fields` - return a list of all **place** object fields.
* `return_poll_fields` - return a list of all **poll** object fields.
* `return_tweet_fields` - return a list of all **tweet** object fields.
* `return_user_fields` - return a list of all **user** object fields.

Show Methods:
* `show_media_fields` - print a list of all **media** object fields, and a link to the reference page on developer.twitter.com.
* `show_place_fields` - print and list of all **place** object fields, and a link to the reference page on developer.twitter.com.
* `show_poll_fields` - print and list of all **poll** object fields, and a link to the reference page on developer.twitter.com.
* `show_tweet_fields` - print and list of all **tweet** object fields, and a link to the reference page on developer.twitter.com.
* `show_user_fields` - print and list of all **user** object fields, and a link to the reference page on developer.twitter.com.

Returning a list:
```python
from osometweet.utils import ObjectFields as o_fields

# Return a list of all available tweet object fields
all_tweet_object_fields = o_fields.return_tweet_fields()
print(all_tweet_object_fields)
```
which prints
```python
['attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'organic_metrics', 'possiby_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'source', 'text', 'withheld']
```
If you want to query Twitter for all tweet object parameters, you can use this method to create a list of all parameters, and feed that list into whatever method you are utilizing.

Perhaps you don't want all fields, but are not sure which ones you want. Or perhaps you just want to double check something about one of the object field parameters. In that case, the `show_object_fields` methods come in handy.

For example
```python
from osometweet.utils import ObjectFields as o_fields

# This automatically prints all available fields as well as a reference link
# to learn more about each field.
o_fields.show_tweet_fields()
```
which prints (no print function necessary)
```python
Twitter V2 Available Tweet Fields:
-attachments
-author_id
-context_annotations
-conversation_id
-created_at
-entities
-geo
-id
-in_reply_to_user_id
-lang
-non_public_metrics
-organic_metrics
-possiby_sensitive
-promoted_metrics
-public_metrics
-referenced_tweets
-reply_settings
-source
-text
-withheld
-Reference: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
```

The exact same procedure can be utilized for all of the methods listed [here](#o_utilsobjectfields).

---