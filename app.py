import time
import redis
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask("app")

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Redis host: {}, Redis port: {} . Hello World! I have been seen {} times.\n'.format(REDIS_HOST, REDIS_PORT, count)