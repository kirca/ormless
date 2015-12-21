from ormless import *
from annotations import types
from functools import partial
from collections import namedtuple


ANamedTuple = partial(namedtuple, 'ANamedTuple')


class AClass:
    attr1 = 'abc'
    attr2 = 100


@convert
@types(ANamedTuple(['attr1', 'attr2']))
def f(arg1):
    return arg1


def test_convert():
    arg_type = f.__annotations__['arg1']
    converted_type = f(A())
    assert isinstance(converted_type, arg_type), "The argument is not converted"


