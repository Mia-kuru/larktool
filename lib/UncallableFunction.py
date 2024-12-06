"""class uncallable function

"""
class _PendingFunction():
    def __init__(self, func, args, kwargs) -> None:
        self.__item = func
        self.__argc = (args, kwargs)

    def _To_Res(self):
        """see the raw code"""
        # To confuse User so that they do not know that it is real call api
        if not callable(self.__item):
            raise TypeError("%s can't be called" % self.__item)
        return self.__item(*self.__argc[0], **self.__argc[1])

    def __call__(self, *args, **kwds):
        return self

class UncallableFunction():
    def __init__(self, func, wrapper=None) -> None:
        if wrapper is not None:
            self.__item = wrapper(func)
        else:
            self.__item = func

    def __call__(self, *args, **kwds) -> _PendingFunction:
        return _PendingFunction(self.__item, args, kwds)

def run_uncallable(uncallable_func):
    """run the uncallable function which was decoated `uncallable`"""
    if isinstance(uncallable_func, UncallableFunction):
        raise TypeError("`uncallable_func` must be interface wrapper as a UncallableFunation.")
    return uncallable_func._To_Res()

def uncallable(func):
    """being an uncallable function.
    call uncallable function well return a UncallableFunation, or not run the func.
    you can use run_func

    Using:
        @uncallable
        def func(): ...
    or you can use to the encapsulation function and 
        `return uncallable(func)`
    """
    return UncallableFunction(func)

def uncallableWrapper(wrapper):
    """being an uncallable function.
    call uncallable function well return a UncallableFunation, or not run the func.
    you can give a custom wrapper.

    Using:
        @uncallableWrapper(yourWrapper)
        def func(): ...
    or you can use to the encapsulation function and 
        `return uncallableWrapper(yourWrapper)(func)`
    """
    def wrap(func):
        return UncallableFunction(func, wrapper)
    return wrap