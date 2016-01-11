from ormless import *
from annotations import types
from functools import partial
from collections import namedtuple
from utils import flip


ANamedTuple = partial(namedtuple, 'ANamedTuple')

class AClass:
    attr1 = 'abc'
    attr2 = 100


def test_convert_one():
    @convert
    @types(ANamedTuple(['attr1', 'attr2']))
    def f(arg1):
        return arg1

    arg_type = f.__annotations__['arg1']
    converted_arg = f(AClass())
    assert isinstance(converted_arg, arg_type), (
        "The argument is not converted")


def test_convert_only_first():
    @convert
    @types(ANamedTuple(['attr1', 'attr2']))
    def f(arg1, arg2):
        return arg1, arg2

    arg1_type = f.__annotations__['arg1']
    arg1 = AClass()
    arg2 = 'test'
    converted_arg1, returned_arg2 = f(arg1, arg2)
    assert isinstance(converted_arg1, arg1_type), (
        "The first argument is not converted")
    assert arg2 == returned_arg2, (
        "The second argument is changed")


def test_convert_multi():
    @convert
    @types(ANamedTuple(['attr1', 'attr2']))
    def f(arg1):
        return arg1

    arg_type = f.__annotations__['arg1']
    converted_args = f([AClass(), AClass()])
    is_arg_type = partial(flip(isinstance), arg_type)
    assert len(converted_args), (
        "Arguments are missing")
    assert all(map(is_arg_type, converted_args)), (
        "Not all argument are converted")


def test_convert_kwargs():
    @convert
    @types(kwarg1=ANamedTuple(['attr1', 'attr2']))
    def f(kwarg1=None):
        return kwarg1

    kwarg_type = f.__annotations__['kwarg1'] 
    converted_kwarg = f(AClass())
    assert isinstance(converted_kwarg, kwarg_type), (
        "The keyword argument is not converted")


def test_convert_only_first_kwarg():
    @convert
    @types(ANamedTuple(['attr1', 'attr2']))
    def f(kwarg1=None, kwarg2=None):
        return kwarg1, kwarg2

    kwarg1_type = f.__annotations__['kwarg1']
    kwarg1 = AClass()
    kwarg2 = 'test'
    converted_kwarg1, returned_kwarg2 = f(kwarg1=kwarg1,
                                          kwarg2=kwarg2)
    assert isinstance(converted_kwarg1, kwarg1_type), (
        "The first keyword argument is not converted")
    assert kwarg2 == returned_kwarg2, (
        "The second keyword argument is changed")


ATypedNamedTuple = partial(typed, partial(namedtuple, 'ANamedTuple1'))


class AParentClass:
    attr1 = 'efg'
    attr2 = AClass()


def test_convert_one_typed():
    @convert
    @types(
        ATypedNamedTuple(
            ['attr1', 'attr2'],
            {'attr1': str,
             'attr2' : ANamedTuple(['attr1', 'attr2']),
             }))
    def f(arg1):
        return arg1

    arg_type = f.__annotations__['arg1']
    arg_field_type = arg_type._field_types['attr2']
    converted_arg = f(AParentClass())
    assert isinstance(converted_arg, arg_type), (
        "The argument is not converted")
    assert isinstance(converted_arg.attr2, arg_field_type), (
        "The argument's field is not converted")
