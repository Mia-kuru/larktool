class Signletype(type):
    """Metaclass only one self"""
    _instance = None
    def __call__(self, *args, **kwds) -> type:
        if not self._instance:
            self._instance:type = super().__call__(*args, **kwds)
        return self._instance

class signleton(metaclass=Signletype):
    """Singleton type. 
    
    Using: 
        class ClassA(signleton): ...
    """