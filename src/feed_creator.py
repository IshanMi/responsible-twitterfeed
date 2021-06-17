import tweepy


def get_api(api_key, secret_key):
    auth = tweepy.AppAuthHandler(consumer_key=api_key, consumer_secret=secret_key)
    return tweepy.API(auth)


def get_tweets(api: tweepy.API, query: str, limit=10):
    return [t.text for t in tweepy.Cursor(api.search, q=query).items(limit)]


def testing():
    pass


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
