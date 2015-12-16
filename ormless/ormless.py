
from functools import wraps


def tuplize(ntuple, objects, attrs):
    ntuple = ntuple(attrs)
    return (ntuple._make(map(partial(getattr, obj), attrs))
            for obj in objects)    

def uses(attrs):
    """
    Decorator serializing an object in 
    
    :param attrs: list of tuples containg the set of attributes
                  that will be used the wrapped function
                  Example [('name', 'age'), ]
    """
    def uses_decorator(func):
        @wraps
        def func_wrapper(*args, **kwargs):
            return 
        pass
    
    pass
