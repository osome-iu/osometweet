import sys
import os
import unittest
import osometweet

api_key = os.environ.get('API_KEY', '')
api_key_secret = os.environ.get('API_KEY_SECRET', '')
access_token = os.environ.get('ACCESS_TOKEN', '')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET', '')
bearer_token = os.environ.get("BEARER_TOKEN")

class TestOauth(unittest.TestCase):
    """
    Make sure the oatuh is working
    """
    def test_1a(self):
        ot = osometweet.OsomeTweet(
            api_key=api_key,
            api_key_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        test_tweet_id = '1323314485705297926'
        resp = ot.tweet_lookup(tids=[test_tweet_id])
        self.assertEqual(resp['data'][0]['id'], test_tweet_id)
    
    def test_2(self):
        ot = osometweet.OsomeTweet(bearer_token=bearer_token)
        test_tweet_id = '1323314485705297926'
        resp = ot.tweet_lookup(tids=[test_tweet_id])
        self.assertEqual(resp['data'][0]['id'], test_tweet_id)

class TestAPI(unittest.TestCase):
    """
    Test all the API endpoints
    """
    def setUp(self):
        self.ot = osometweet.OsomeTweet(bearer_token=bearer_token)

    def test_tweet_lookup(self):
        test_tweet_ids = ['1323314485705297926', '1328838299419627525']
        resp = self.ot.tweet_lookup(tids=test_tweet_ids)
        for tweet in resp['data']:
            self.assertIn(tweet['id'], test_tweet_ids) 
    
    def test_user_lookup_ids(self):
        test_user_ids = ['12', '13']
        resp = self.ot.user_lookup_ids(test_user_ids)
        for user in resp['data']:
            self.assertIn(user['id'], test_user_ids) 

    def test_user_lookup_usernames(self):
        test_user_usernames = ['jack', 'biz']
        resp = self.ot.user_lookup_usernames(test_user_usernames)
        for user in resp['data']:
            self.assertIn(user['username'], test_user_usernames) 


if __name__ == "__main__":
    unittest.main()