#!/usr/bin/env python3
"""
Module Writting to redis
"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """
    Redis client object
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using random key and return the key
        """
        randomkey = str(uuid4())
        self._redis.set(randomkey, data)

        return randomkey
