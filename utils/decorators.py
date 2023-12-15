from functools import wraps
from typing import Callable


def singleton(class_):
    instance = [None]

    @wraps(class_)
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = class_(*args, **kwargs)
        return instance[0]

    return wrapper


def lock_thread(locker):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with locker:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def catch_exception(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)

    return wrapper
