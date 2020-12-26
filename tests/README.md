# Introduction

This folder contains the unit tests for the package.

# How to run?

You will need a set of valid Twitter developer app keys for the V2 API, export the keys and secrets using the following commands:

```sh
export 'API_KEY'='YOUR_TWITTER_API_KEY'
export 'API_KEY_SECRET'='YOUR_TWITTER_API_KEY_SECRET'
export 'ACCESS_TOKEN'='YOUR_TWITTER_ACCESS_TOKEN'
export 'ACCESS_TOKEN_SECRET'='YOUR_TWITTER_ACCESS_TOKEN_SECRET'
export 'BEARER_TOKEN'='YOUR_TWITTER_BEARER_TOKEN'
```

Then just run:

```sh
python tests.py
```