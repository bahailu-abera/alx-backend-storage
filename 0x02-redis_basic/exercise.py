#!/usr/bin/env python3
"""
Module Writting to redis
"""
from functools import wraps
import redis
from uuid import uuid4
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    A decorator function
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """
    Redis client object
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using random key and return the key
        """
        randomkey = str(uuid4())
        self._redis.set(randomkey, data)

        return randomkey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[bytes, float, int, str]:
        """
        Convert the data to the desired format
        """
        value = self._redis.get(key)
        if fn is None or value is None:
            return value
        return fn(value)

    def get_str(self, key: str) -> str:
        """
        Get a string from the cache
        """
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Get an int from the cache
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
