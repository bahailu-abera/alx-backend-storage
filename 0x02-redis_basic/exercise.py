#!/usr/bin/env python3
"""
Module Writting to redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Redis client object
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> uuid.UUID:
        """
        Store the input data in Redis using random key and return the key
        """
        key = uuid.uuid4()
        self._redis.set(str(key), data)

        return str(key)
