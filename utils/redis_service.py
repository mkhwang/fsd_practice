import os

from redis import Redis


class RedisService:
    def __init__(self):
        self.redis_client = Redis.from_url(
            f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/0"
        )

    def set(self, key, value, ex=None):
        self.redis_client.set(key, value, ex=ex)

    def get(self, key):
        return self.redis_client.get(key)

    def delete(self, key):
        self.redis_client.delete(key)

    def exists(self, key):
        return self.redis_client.exists(key)

    def keys(self, pattern):
        return self.redis_client.keys(pattern)
