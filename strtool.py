import re

__all__ = ["reNoneType", "replaces_all", 
           "re_compiler"]

class reNoneType():
    """Using:
        >>> (re.serach() or reNoneType).group()
        # if not match, it equal to `""`
    """
    @staticmethod
    def group(_=None):
        return ''

def replaces_all(string:str, pattens=None, repl=None):
    """replace mutil"""
    if isinstance(pattens, str):
        return string.replace(pattens, repl)
    for patten in pattens:
        string = string.replace(patten, repl)
    return string

def re_compiler(str_, compiler, group=1, mode='search'):
    """Match and return the matched group directly, 
    without judging whether it is None or not.

    Using:
        >>> find_abc = re.compile("(abc)")
        >>> res = re_compiler("Aabc", find_abc)
        # res == 'abc' if res is None return None

        if you don't use re_compiler, and you want get the group.
        Before you can `res.group(1)`, You need judging whether res is None.
        >>> res = find_abc.search("Aabc")
        # res == 'Aabc'. you should group(1)
        >>> res = find_abc.search("Aabd")
        # res == None. you can't group()

    Args:
        _str (str): it will be matched by re.search or re.match

        compiler (Pattern): re.compile()'s rtype.

        group (int, str): matched index or name. Defaults to 1.

        mode (str): you can select 'search' or 'match'. 
            Defaults to 'search'.

    Returns:
        str|None: if match right! it return str, else return None.
    """
    if mode in ['search', 'match']:
        re_method = getattr(compiler, mode)
        res = re_method(str(str_))
    else:
        raise ValueError("%s is not defind. " 
                    "Did you mean 'search' or 'match'?" % mode)
    if res is not None:
        try:
            if '(' not in compiler.pattern:
                group = 0
            return res.group(group)
        except AttributeError:
            raise TypeError("compiler is not Pattern")
    else:
        return res

# split
# -----
def split_():
    pass
# join
def join_(values1, values2, center=' ', left=None, right=', '):
    # HACK:
    buffers = []
    for i,j in zip(values1, values2):
        buffers.append(center.join([i, j]))
    return right.join(buffers)
# norm
