import tweepy
import os
from dotenv import load_dotenv, find_dotenv


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # Disconnects the stream
            return False


class TwitterClient:

    def __init__(self):
        load_dotenv(find_dotenv())
        self.auth = tweepy.AppAuthHandler(consumer_key=os.getenv("API_KEY"),
                                          consumer_secret=os.getenv("API_SECRET_KEY"))
        self.api = tweepy.API(self.auth)
        self.streams = []
        self.stream_listener = None
        self.stream = None

    def get_tweets(self, query: str, limit=20):
        # .encode('ascii', errors='ignore')
        return [t.full_text for t in tweepy.Cursor(self.api.search, q=query, tweet_mode='extended').items(limit)]

    def start_stream(self):
        # Ensure only one stream is active at a time
        for stream in self.streams:
            stream.disconnect()

        self.stream_listener = MyStreamListener()
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.stream_listener)



