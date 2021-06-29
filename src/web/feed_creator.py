import tweepy
import os
from dotenv import load_dotenv, find_dotenv
from json import loads
from time import time
from src.database.tweet import Tweet


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, session, limit=10):
        self._session = session
        self.start_time = time()
        self.timeout = limit

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # Disconnects the stream
            return False
        else:
            print(f'Error code: {status_code}')
            return False

    def on_data(self, raw_data):
        tweet_data = loads(raw_data)

        if time() - self.start_time > self.timeout:
            # End the stream after a given amount of time
            return False
        else:
            try:
                new_tweet = Tweet()
                new_tweet.text = tweet_data['text']
            except KeyError:
                return True

            new_tweet.tweet_id = tweet_data['id']
            new_tweet.id_str = tweet_data['id_str']
            new_tweet.time = tweet_data['created_at']

            # Add this Tweet to DB
            self._session.add(new_tweet)
            self._session.commit()
            return True


class TwitterClient:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.auth = tweepy.OAuthHandler(consumer_key=os.getenv("API_KEY"), consumer_secret=os.getenv("API_SECRET_KEY"))
        access_token = os.getenv("ACCESS_TOKEN")
        access_secret_token = os.getenv("ACCESS_TOKEN_SECRET")
        self.auth.set_access_token(access_token, access_secret_token)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.streams = []
        self.stream = None

        try:
            self.redirect_url = self.auth.get_authorization_url()
        except tweepy.TweepError:
            print("Error- Unable to get request token")

    def get_tweets(self, query: str, limit=20):
        return [t.full_text.encode('ascii', errors='ignore') for t in
                tweepy.Cursor(self.api.search, q=query, tweet_mode='extended').items(limit)]

    def start_stream(self, factory):
        # Disconnect all previous streams
        for s in self.streams:
            s.disconnect()

        # Create new stream
        self.stream = tweepy.Stream(self.auth, MyStreamListener(session=factory))
        self.streams.append(self.stream)
