import redis
from rq import Worker, Queue, Connection
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
redis_url = os.getenv('REDIS_URL')
conn = redis.from_url(redis_url)

listen = ['default']


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
