from math import ceil

STYLE = {
    "dict-0":"|{:{}} : {:{}} ",
    "dict-1":"| {:{}} : {:{}} | ",
    "dict-2":"|{:{}} ",
}

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
    min_key_length = [min((len(key) for key in col)) for col in cols]
    max_value_length = [max((len(str(dt[key])) for key in col)) for col in cols]

    lines = ['']*rows

    for kl, mkl, vl, col in zip(max_key_length, min_key_length, max_value_length, cols):
        for i, key in enumerate(col):
            # TODO: 动态调整key和值的大小，当最大键与最小键大于5时，按最小键小于的第n个5倍为界限

            # HACK: 下面实现不完善
            # nkl = len(key)
            # if kl - nkl > 3:
            #     vl_ = vl + kl - nkl - 2
            #     kl_ = nkl + 2
            # else:
            #     kl_, vl_ = kl, vl
            # lines[i] += STYLE["dict-0"].format(key, kl_, str(dt[key]), vl_)
            
            lines[i] += STYLE["dict-0"].format(key, kl, str(dt[key]), vl)
            # 键不对齐
            # lines[i] += STYLE["dict-2"].format(' = '.join((key, str(dt[key]))), kl+vl+3)

    return "\n".join(lines)