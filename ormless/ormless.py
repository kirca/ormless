
from functools import wraps, partial
from itertools import starmap, ifilterfalse
from operator import contains


def tuplize(ntuple, attrs, obj):
    return ntuple._make(map(partial(getattr, obj), attrs))


def convert(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        def _convert(key, arg):
            arg_type = func.__annotations__[key]
            if hasattr(arg_type, '_fields'):
                _tuplize = partial(tuplize, arg_type, arg_type._fields)
                if hasattr(arg, '__iter__'):
                    return (key, map(_tuplize, arg))
                return (key, _tuplize(arg))
            return (key, arg)
        
        kwargs = dict(starmap(_convert, kwargs.items()))
        arg_names = ifilterfalse(partial(contains, kwargs.keys()), func.__code__.co_varnames)
        args = tuple(map(lambda x: x[1], starmap(_convert, zip(arg_names, args))))
        return func(*args, **kwargs)
    return func_wrapper
