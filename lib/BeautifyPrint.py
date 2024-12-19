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
    return re.match(r'^[0-9a-fA-F]{6}$', value) is not None

def is_256_color(value):
    if not str(value).isdigit():
        return False
    return int(value) < 256 and int(value) >= 0

def hex_to_rgb10(hex_value):
    # Converts hexadecimal color values to decimal rgb, 
    # Return a tuple of the form (r, g, b)
    if isinstance(hex_value, str):
        hex_value = hex_value.lstrip('#')
        if not is_hex_color(hex_value):
            raise ValueError("%s is not a valid hex color"
                             % hex_value)
    else:
        raise TypeError("Input must be a str.")

    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)

    return (r, g, b)

def rgb10_to_hex(r, g, b):
    if not all(isinstance(i, int) for i in (r, g, b)):
        raise ValueError("All inputs must be integers.")

    r, g, b = abs(r), abs(g), abs(b)
    hex_value = ''.join(f"{item:02x}" for item in (r, g, b))
    return hex_value

class _CSIcolorMeta(type):
    def __getattr__(cls, name):
        color = None

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
    """Escape code contorl color calss"""
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

def default_display():
    """Restore default print display"""
    sys.stdout.write(CSIcolor.default)

def newline(n=1):
    """Prints a specified number of newlines."""
    sys.stdout.write("\n"*n)

def clearline():
    """Set print at the beginning of the current line,
    and clear current line buffer."""
    sys.stdout.write(esc_code['clear_line'])
    sys.stdout.flush()

def _get_color_prefix(color, rgb, **kwargs):
    color_prefix = ""
    brgb = kwargs.get("brgb", None)

    f_color = color or kwargs.get("c", None)
    b_color = None

    if rgb is not None:
        f_color = rgb10_to_hex(*rgb)
    if brgb is not None:
        b_color = "b_" + rgb10_to_hex(*brgb)

    if f_color is not None:
        color_prefix += getattr(CSIcolor, f_color)
    if b_color is not None:
        color_prefix += getattr(CSIcolor, b_color)

    return color_prefix

def set_color(color=None, rgb=None, brgb=None, **kwargs):
    """Set print display color

    Args:
        color (str, optional): Color name from [red, blue, black, white
            , green, yellow, cyanine, amaranth] or 
            a 16-bit hex RGB string (e.g., 'ff00ff'). If prefixed with "b_", 
            it sets the background color. Defaults to None.
        rgb (tuple, optional): A tuple (r, g, b) representing an RGB color. 
            Defaults to None.
        brgb (tuple, optional): A tuple (r, g, b) representing 
            a background RGB color. Defaults to None.
    """
    color_prefix = _get_color_prefix(color, rgb, brgb=brgb, **kwargs)
    if color_prefix == '':
        color_prefix = CSIcolor.default
    sys.stdout.write(color_prefix)

def _print(
        *values: object,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False
    ):
    """Equal print, but this performance is better"""
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
        restore=True, 
        **kwargs
    ):
    """
    Prints values with optional color formatting.

    Args:
        *values: Arbitrary number of objects to print.
        color (str, optional): Color name from [red, blue, black, white
            , green, yellow, cyanine, amaranth] or 
            a 16-bit hex RGB string (e.g., 'ff00ff'). If prefixed with "b_", 
            it sets the background color. Defaults to None.
        rgb (tuple, optional): A tuple (r, g, b) representing an RGB color. 
            Defaults to None.
        sep (str, optional): Separator between values. 
            Defaults to " ".
        end (str, optional): Added in the last line.
            Defaults to "\\n".
        flush (bool, optional): Whether to flush the output buffer. 
            Defaults to True.
        restore (bool): Restore default print color.
            Defaults to True.
    """
    set_color(color=color, rgb=rgb, **kwargs)
    _print(*values, sep=sep, end=end, flush=flush)
    if restore: default_display()

def inline_print(
        *values, 
        color=None, 
        rgb=None, 
        brgb=None, 
        line_color=False,
        flush=True, 
        sep=" ", 
        **kwargs
    ):
    """
    Prints values on the same line with optional color formatting.

    Args:
        *values: Arbitrary number of objects to print.
        color (str, optional): Color name from [red, blue, black, white
            , green, yellow, cyanine, amaranth] or 
            a 16-bit hex RGB string (e.g., 'ff00ff'). If prefixed with "b_", 
            it sets the background color. Defaults to None.
        rgb (tuple, optional): A tuple (r, g, b) representing an RGB color. 
            Defaults to None.
        brgb (tuple, optional): A tuple (r, g, b) representing 
            a background RGB color. Defaults to None.
        line_color (bool): The whole row becomes the background color.
            Defaults to False.
        flush (bool, optional): Whether to flush the output buffer. 
            Defaults to True.
        sep (str, optional): Separator between values. 
            Defaults to " ".
    """
    if line_color:
        set_color(color=color, rgb=rgb, brgb=brgb, **kwargs)
    clearline()
    clprint(*values, color=color, rgb=rgb, brgb=brgb
            , sep=sep, end='', flush=flush, **kwargs)