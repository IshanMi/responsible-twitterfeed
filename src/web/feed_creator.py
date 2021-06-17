import tweepy
import os
from dotenv import load_dotenv, find_dotenv
from json import loads


def _log_tweet(tweet, file='tweets.txt'):
    with open(file, 'a', encoding="utf-8") as f:
        f.write(tweet)
        f.write("\n")
    return None


class MyStreamListener(tweepy.StreamListener):

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
        a = loads(raw_data)
        if 'text' not in a:
            print(a)
        _log_tweet(tweet=a['text'], file='db_placeholder.txt')
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

    def start_stream(self):
        self.stream = tweepy.Stream(self.auth, MyStreamListener())
        self.streams.append(self.stream)
