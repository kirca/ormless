from functools import wraps


def flip(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = tuple(reversed(args))
        return func(*args, **kwargs)
    return wrapper
