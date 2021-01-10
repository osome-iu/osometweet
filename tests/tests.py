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
    Make sure the oauth is working
    """
    def test_1a(self):
        oauth1a = osometweet.OAuth1a(
            api_key=api_key,
            api_key_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        test_tweet_id = '1323314485705297926'
        resp = oauth1a.make_request(
            'https://api.twitter.com/2/tweets',
            {"ids": f"{test_tweet_id}"}
            ).json()
        self.assertEqual(resp['data'][0]['id'], test_tweet_id)
    
    def test_1a_exception(self):
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(api_key=1)
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(api_key_secret=1)
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(access_token=1)
        with self.assertRaises(ValueError):
            osometweet.OAuth1a(access_token_secret=1)
    
    def test_2(self):
        oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
        test_tweet_id = '1323314485705297926'
        resp = oauth2.make_request(
            'https://api.twitter.com/2/tweets',
            {"ids": f"{test_tweet_id}"}
            ).json()
        self.assertEqual(resp['data'][0]['id'], test_tweet_id)
    
    def test_2_exception(self):
        with self.assertRaises(ValueError):
            osometweet.OAuth2(bearer_token=1)

class TestAPI(unittest.TestCase):
    """
    Test all the API endpoints
    """
    def setUp(self):
        oauth2 = osometweet.OAuth2(bearer_token=bearer_token)
        self.ot = osometweet.OsomeTweet(oauth2)

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
    
    def test_get_followers(self):
        resp = self.ot.get_followers('12')
        self.assertEqual(resp['meta']['result_count'], len(resp['data']))

        resp_2 = self.ot.get_followers(
            '12',
            pagination_token=resp['meta']['next_token'],
            max_results=10
        )
        self.assertEqual(10, len(resp_2['data']))

    def test_get_following(self):
        resp = self.ot.get_following('12')
        self.assertEqual(resp['meta']['result_count'], len(resp['data']))

        resp_2 = self.ot.get_followers(
            '12',
            pagination_token=resp['meta']['next_token'],
            max_results=10
        )
        self.assertEqual(10, len(resp_2['data']))

if __name__ == "__main__":
    unittest.main()