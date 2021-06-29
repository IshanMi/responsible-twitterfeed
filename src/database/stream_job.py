from src.web.feed_creator import TwitterClient


def stream_job(client: TwitterClient, factory, queries: list):
    client.start_stream(factory)
    client.stream.filter(
        track=queries,
        languages=['en'],
        is_async=True
    )
