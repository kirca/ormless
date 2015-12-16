

def _func_annotation_for(func):
    """Retrieve the function annotation for a given function or create it"""
    current = getattr(func,'__annotations__',None)
    if current is None:
        current = func.__annotations__ = {}
    return current


def types( *types, **named ):
    def annotate(function):
        base = _func_annotation_for(function)
        base.update(named)
        if hasattr( function, 'func_code' ): # python 2.x
            names = function.func_code.co_varnames
        else:
            names = function.__code__.co_varnames
        
        for name, typ in zip(names, types):
            base[name] = typ
        return function 
    return annotate


def returns( typ ):
    def annotate(function):
        _func_annotation_for(function)['return'] = typ 
        return function 
    return annotate