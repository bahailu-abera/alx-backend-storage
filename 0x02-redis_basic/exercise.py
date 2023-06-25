#!/usr/bin/env python3
"""
Module Writting to redis
"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    """
    Redis Client Object
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, str, float, bytes]) -> str:
        """
        Stores the input data in a redis with a random key
        and returns the key
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key
