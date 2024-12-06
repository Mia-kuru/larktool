import re
import shutil

__all__ = ["color", "DISPLAY", "reNoneType", "replaces_all", 
           "re_compiler"]

# Escape CSI code

DEFAULT = '\x1b[0m'

# display
DISPLAY = {
    "highlight"  : '\x1b[1m',
    "overlink"   : '\x1b[4m',
    "blink"      : '\x1b[5m',
    "white_light": '\x1b[7m',
    "invisible"  : '\x1b[8m'
}

# color
COLOR = {
    'default' :    DEFAULT,
    'red'     : '\x1b[31m',
    'blue'    : '\x1b[34m',
    'black'   : '\x1b[30m',
    'white'   : '\x1b[37m',
    'green'   : '\x1b[32m',
    'yellow'  : '\x1b[33m',
    'cyanine' : '\x1b[36m',
    'amaranth': '\x1b[35m'
}

# color background
BACKGROUND = {
    "black"   : '\x1b[40m',
    "red"     : '\x1b[41m',
    "green"   : '\x1b[42m',
    "yellow"  : '\x1b[43m',
    "blue"    : '\x1b[44m',
    "amaranth": '\x1b[45m',
    "cyanine" : '\x1b[46m',
    "white"   : '\x1b[47m'
}

class color:
    """Use simple escape color"""
    default    =  COLOR['default']
    red        =  COLOR['red']
    blue       =  COLOR['blue']
    black      =  COLOR['black']
    white      =  COLOR['white']
    green      =  COLOR['green']
    yellow     =  COLOR['yellow']
    cyanine    =  COLOR['cyanine']
    amaranth   =  COLOR['amaranth']
 
    b_red      =  BACKGROUND['red']
    b_blue     =  BACKGROUND['blue']
    b_black    =  BACKGROUND['black']
    b_white    =  BACKGROUND['white']
    b_green    =  BACKGROUND['green']
    b_yellow   =  BACKGROUND['yellow']
    b_cyanine  =  BACKGROUND['cyanine']
    b_amaranth =  BACKGROUND['amaranth']

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
