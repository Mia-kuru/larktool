"""Preset param

"""
def warp_preset_param1(func):
    """
    Fix the param1

    Using:
        @warp_preset_param1
        def func(param1, param2):
            ...
        def func2(func_):
            ...

        >>> func2(func("A"))
        # In func2, call func_("B") equal to call func("A", "B").
    """
    def give_param1(param1):
        def give_param2(param2):
            return func(param1, param2)
        return give_param2
    return give_param1

def warp_preset_param2(func):
    """
    Fix the param2
    
    Using:
        @warp_preset_param2
        def func(param1, param2):
            ...
        def func2(func_):
            ...

        >>> func2(func("A"))
        # In func2, call func_("B") equal to call func("B", "A").
    """
    def give_param2(param2):
        def give_param1(param1):
            return func(param1, param2)
        return give_param1
    return give_param2