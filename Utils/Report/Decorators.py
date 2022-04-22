"""
@Time ： 2022/4/21 14:08
@Auth ： Ted
@File ：Decorators.py
@IDE ：PyCharm
"""
from functools import wraps


def group_name(name: str):

    def wrap(cls):
        cls.__doc__ = name
        return cls

    return wrap


def case_name(name: str):
    def decorator(func):
        @wraps(func)
        def set_case_name(*args, **kwargs):
            tmp = args[0]
            tmp._testMethodDoc = name
            return func(*(tmp, *args[1:]), **kwargs)
        return set_case_name
    return decorator







