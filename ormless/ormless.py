from functools import wraps, partial
from itertools import starmap, ifilterfalse
from operator import contains


def tuplize(ntuple, attrs, obj):
    return ntuple._make(map(partial(getattr, obj), attrs))


def convert(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        def get_second(iterable):
            return iterable[1]

        def _convert(key, arg):
            arg_type = func.__annotations__[key]
            if hasattr(arg_type, '_fields'):
                _tuplize = partial(tuplize, arg_type, arg_type._fields)
                if hasattr(arg, '__iter__'):
                    return (key, map(_tuplize, arg))
                return (key, _tuplize(arg))
            return (key, arg)

        in_kwarg_names = partial(contains, kwargs.keys())
        in_annotations = partial(contains, func.__annotations__)

        def in_annotations_kwarg(kwarg):
            kwarg_name, kwarg_value = kwarg
            return in_annotations(kwarg_name)

        typed_kwargs = filter(in_annotations_kwarg, kwargs.items())
        left_kwargs = dict(list(
            set(kwargs.items()) -
            set(typed_kwargs)))
        kwargs = dict(starmap(_convert, typed_kwargs))
        kwargs.update(left_kwargs)

        arg_names = filter(in_annotations,
                           ifilterfalse(in_kwarg_names,
                                        func.__code__.co_varnames))
        left_args = list(args[len(arg_names):])
        args = tuple(map(get_second,
                         starmap(_convert, zip(arg_names, args)))
                     + left_args)

        return func(*args, **kwargs)
    return func_wrapper
