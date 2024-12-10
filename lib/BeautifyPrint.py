from math import ceil
import re
import os
import sys

enable_ansi_control = False

def enable_ansi():
    global enable_ansi_control
    if os.name == "nt":
        from ctypes import windll, c_int, byref

        hStdOut = windll.kernel32.GetStdHandle(c_int(-11))
        mode = c_int(0)
        windll.kernel32.GetConsoleMode(c_int(hStdOut), byref(mode))
        mode.value |= 0x0004
        windll.kernel32.SetConsoleMode(c_int(hStdOut), mode)

        enable_ansi_control = True

if not enable_ansi_control:
    enable_ansi()

STYLE = {
    "dict-0":"|{:{}} : {:{}} ",
    "dict-1":"| {:{}} : {:{}} | ",
    "dict-2":"|{:{}} ",
}

# '\r' will immediately flush buffer to print, 
# but '\x1b[0G' will not flush buffer to print.
CLEAR_LINE = "\r\x1b[K"

# Escape CSI code
# Wiki: https://en.wikipedia.org/wiki/ANSI_escape_code
esc_code = {
    "default_display" : '\x1b[0m',
    "set_display" : {
        "highlight"  : '\x1b[1m',
        "overlink"   : '\x1b[4m',
        "blink"      : '\x1b[5m',
        "white_light": '\x1b[7m',
        "invisible"  : '\x1b[8m'
    },
    "color" : {
        'red'     : '\x1b[31m',
        'blue'    : '\x1b[34m',
        'black'   : '\x1b[30m',
        'white'   : '\x1b[37m',
        'green'   : '\x1b[32m',
        'yellow'  : '\x1b[33m',
        'cyanine' : '\x1b[36m',
        'amaranth': '\x1b[35m'
    },
    "background_color" : {
        "black"   : '\x1b[40m',
        "red"     : '\x1b[41m',
        "green"   : '\x1b[42m',
        "yellow"  : '\x1b[43m',
        "blue"    : '\x1b[44m',
        "amaranth": '\x1b[45m',
        "cyanine" : '\x1b[46m',
        "white"   : '\x1b[47m'
    },
    "set_color" : {
        "foreground" : 38,
        "background" : 48,
        "256_color"  : "\x1b[{mode};5;{value}m",
        "rgb"        : "\x1b[{mode};2;{r};{g};{b}m",
    },
    "cursor_control" : {
        "up"        : '\x1b[{n}A',
        "down"      : '\x1b[{n}B',
        "forward"   : '\x1b[{n}C',
        "back"      : '\x1b[{n}D',
        "next_line" : '\x1b[{n}E',
        "previous_line"   : '\x1b[{n}F',
        "online_absolute" : '\x1b[{n}G',
        "set_position" : '\x1b[{x};{y}H',
    },
    "clear_line"   : '\x1b[0G\x1b[K',
    "clear_screen" : '\x1b[2J\x1b[0;0H'
}

def is_hex_color(value):
    return re.match(r'^[0-9a-fA-F]{6}$', value)

def is_256_color(value):
    if not value.isdigit():
        return False
    return int(value) < 256 and int(value) >= 0

def hex_to_rgb10(hex_value):
    # Converts hexadecimal color values to decimal rgb, 
    # Return a tuple of the form (r, g, b)
    if isinstance(hex_value, str):
        hex_value = hex_value.lstrip('#')

        if not is_hex_color(hex_value):
            raise ValueError("%s is not a hex color" % hex_value)

        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)
    elif isinstance(hex_value, bytes):
        r = int.from_bytes(hex_value[0:1], byteorder='big')
        g = int.from_bytes(hex_value[1:2], byteorder='big')
        b = int.from_bytes(hex_value[2:3], byteorder='big')
    else:
        raise TypeError("Input must be a str or bytes.")

    return (r, g, b)

def rgb10_to_hex(r, g, b):
    return hex(r)[2:] + hex(g)[2:] + hex(b)[2:]

class _CSIcolorMeta(type):
    def __getattr__(cls, name):
        color = None
        # HACK: 
        mode = cls.set_color.get('foreground')
        if name.startswith('b_'):
            name = name[2:]
            mode = cls.set_color.get('background')

        if name in cls.addr_color_names:
            color = cls.addr_color_map.get(name, None)
        elif is_hex_color(name.lstrip('#')):
            r, g, b = hex_to_rgb10(name)
            color = cls.set_color['rgb'].format(
                                            mode=mode, r=r, g=g, b=b)
            return color
        elif is_256_color(name):
            color = cls.set_color['256_color'].format(
                                                mode=mode, value=name)
            return color

        if color is None:
            color = 'default'

        return getattr(cls, color, cls.default)

class CSIcolor(metaclass=_CSIcolorMeta):
    """escape code contorl color calss"""
    default    =  esc_code['default_display']
    red        =  esc_code['color']['red']
    blue       =  esc_code['color']['blue']
    black      =  esc_code['color']['black']
    white      =  esc_code['color']['white']
    green      =  esc_code['color']['green']
    yellow     =  esc_code['color']['yellow']
    cyanine    =  esc_code['color']['cyanine']
    amaranth   =  esc_code['color']['amaranth']
 
    b_red      =  esc_code["background_color"]['red']
    b_blue     =  esc_code["background_color"]['blue']
    b_black    =  esc_code["background_color"]['black']
    b_white    =  esc_code["background_color"]['white']
    b_green    =  esc_code["background_color"]['green']
    b_yellow   =  esc_code["background_color"]['yellow']
    b_cyanine  =  esc_code["background_color"]['cyanine']
    b_amaranth =  esc_code["background_color"]['amaranth']

    addr_color_names = ['r', 'b', 'g', 'y', 'w']

    addr_color_map = {
        'r' : 'red',
        'b' : 'blue',
        'g' : 'green',
        'y' : 'yellow',
        'w' : 'white'
    }

    # set rgb color and 256 color
    # mode is key == ["foreground", "background"] value
    set_color = esc_code['set_color']


def print_float_format(value, precision=3):
    """Return format str of float.

    Args:
        value (float): float value.
        precision (int, optional): float precision. Defaults to 3.

    Returns:
        str: format str of float.
    """
    if isinstance(value, float):
       return "{:.{}f}".format(value, precision)    
    elif isinstance(value, int) or (isinstance(value, str) 
                                    and value.isdigit()):
        return print_float_format(float(value))
    else:
        raise TypeError("%s is not a float" % value)

# print norm

class BeautifyPrint_():
    def __init__(self, value=None, sformat="data"):
        pass

    def __str__(self):
        pass

    def set_type(self):
        pass

    def format_str(self):
        pass

def dict_format(dt, rows=5, max_cols=3, precision=3):
    # HACK: 读取键和分隔键值
    keys = list(dt.keys())
    col_num = int(ceil(len(keys)/rows))
    cols = [keys[rows*i:rows*(i+1)] for i in range(col_num)]

    # HACK: 规范浮点数的精度
    for key in keys:
        value = dt[key]
        if isinstance(value, float):
            dt[key] = print_float_format(value, precision)

    max_key_length = [max((len(key) for key in col)) for col in cols]
    # min_key_length = [min((len(key) for key in col)) for col in cols]
    max_value_length = [max((len(str(dt[key])) for key in col)) for col in cols]

    lines = ['']*rows

    for kl, vl, col in zip(max_key_length, max_value_length, cols):
        for i, key in enumerate(col):
            # TODO: 动态调整key和值的大小，当最大键与最小键大于5时，按最小键小于的第n个5倍为界限
            
            lines[i] += STYLE["dict-0"].format(key, kl, str(dt[key]), vl)

    return "\n".join(lines)

def newline(n=1):
    sys.stdout.write("\n"*n)

def clearline():
    sys.stdout.write(CLEAR_LINE)

def _print(
        *values: object,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False
    ):
    values = sep.join(map(str, values)) + end
    sys.stdout.write(values)
    if flush:
        sys.stdout.flush()

def clprint(
        *values,
        color=None, 
        rgb=None, 
        sep=' ', 
        end='\n', 
        flush=False, 
        **kwargs
    ):
    """print color font, """
    # HACK: 
    keys = kwargs.keys()
    if 'c' in keys:
        color = kwargs.get('c')
    if rgb is not None:
        r, g, b = rgb
        color = rgb10_to_hex(r, g, b)

    if color is not None:
        val = (
            getattr(CSIcolor, color), sep.join(map(str, values))
            , CSIcolor.default
        )
    else:
        val = values
    _print(*val, sep='', end=end, flush=flush)

def inline_info(
        *values, 
        color=None, 
        rgb=None, 
        flush=True, 
        sep=" ", 
        **kwargs
    ):
    clear_line = esc_code['clear_line']
    values = sep.join(map(str, values))
    val = (clear_line, values)
    clprint(*val, color=color, rgb=rgb
            , sep='', end='', flush=flush, **kwargs)