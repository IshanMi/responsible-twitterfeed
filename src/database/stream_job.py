def stream_job(client, queries):
    client.stream.filter(
        track=queries,
        languages=['en'],
        is_async=True
    )
