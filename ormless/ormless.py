from functools import wraps, partial
from itertools import starmap, ifilterfalse, izip
from operator import contains


def get_second(iterable):
    return iterable[1]

def extract_type(arg_type):
    is_collection = False
    if isinstance(arg_type, list):
        if len(arg_type) != 1:
            raise ValueError("The type declaration %s "
                             "is incorrect. If you want to "
                             "specify a collection"
                             "it must be a list of one type."
                             % arg_type)
        arg_type = arg_type[0]
        is_collection = True
    if type(arg_type) is not type:
        raise ValueError("The type declaration %s "
                         "is incorrect. It is not a valid type"
                         % arg_type)
    return (is_collection, arg_type)


def tuplize(ntuple, attrs, obj):
    def apply_to_second(f, tupl):
        return (tupl[0], f(tupl[1]))

    def get_type(attr, val):
        return (attr, val, ntuple._field_types.get(attr))

    def get_val(attr):
        return attr[1]

    def to_tuplize(attr):
        return (
            hasattr(attr[2][0], '_fields')
            if isinstance(attr[2], list)
            else hasattr(attr[2], '_fields'))

    def tuplize_recur(attr):
        attr_name, attr_val, attr_type = attr
        is_collection, attr_type = extract_type(attr_type)
        if is_collection:
            return map(partial(tuplize, attr_type, attr_type._fields),
                       attr_val)
        return tuplize(attr_type, attr_type._fields, attr_val)

    attr_vals = map(partial(getattr, obj), attrs)
    if not hasattr(ntuple, '_field_types'):
        return ntuple._make(attr_vals)

    attrs_with_types = list(
        enumerate(starmap(get_type, izip(attrs, attr_vals))))
    attrs_to_tuplize = filter(lambda x: to_tuplize(x[1]), attrs_with_types)
    attrs_not_tuplize = map(partial(apply_to_second, get_val),
                            ifilterfalse(partial(contains, attrs_to_tuplize), attrs_with_types))
    tuplized_attrs = map(partial(apply_to_second, tuplize_recur), attrs_to_tuplize)
    attr_vals = map(
        get_second,
        sorted(attrs_not_tuplize + tuplized_attrs,
               key=lambda x: x[0]))
    return ntuple._make(attr_vals)


def convert(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        def _convert(key, arg):
            is_collection, arg_type = extract_type(func.__annotations__[key])

            if hasattr(arg_type, '_fields'):
                _tuplize = partial(tuplize, arg_type, arg_type._fields)
                if is_collection:
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


def typed(ntuple, fields, field_types):
    ntuple_class = ntuple(fields)
    typed_cls_name = "%s_typed" % ntuple_class.__name__

    cls_template = (
        "class {cls_name}(ntuple_class):\n"
        "    _field_types = field_types"
        ).format(
        cls_name=typed_cls_name,
        )
    namespace = {
        'ntuple_class': ntuple_class,
        'field_types': field_types,
        }
    exec cls_template in namespace
    typed_ntuple_cls = namespace[typed_cls_name]
    return typed_ntuple_cls
