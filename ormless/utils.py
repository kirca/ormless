# coding=utf-8
#
# This file is part of ORMless (https://github.com/kirca/ormless)
#
# Copyright (c) 2016 Kiril Vangelovski (k.vangelovski@gmail.com)
#
# This Source Code Form is subject to the terms of the MIT License
# If a copy of the licence was not distributed with this file, You can
# obtain one at https://opensource.org/licenses/MIT .

from functools import wraps


def flip(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = tuple(reversed(args))
        return func(*args, **kwargs)
    return wrapper


def get_second(iterable):
    return iterable[1]


def compose(*funcs):
    def _compose(f, g):
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs)