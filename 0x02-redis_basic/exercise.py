#!/usr/bin/env python3
"""
Module Writting to redis
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single method and returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Redis Client Object
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in a redis with a random key
        and returns the key
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn:
            Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Used to convert back to the desired type
        """
        value = self._redis.get(key)

        if fn is None or value is None:
            return value

        return fn(value)

    def get_str(self, key: str) -> str:
        """
        Get a string from the Cache
        """
        value = self._redis.get(key)

        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Get an integer from the Cache
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))

        except ValueError:
            value = 0

        return value
