def is_out_index(indexs, _iterable:list=None, length:int=None) -> bool:
    """General case: checking indexs whether out index of 'list'.
    Args:
        indexs (list[int] | int): it will be judged whether out index.

        _iterable (list): In general, here input a list.

        length (int): list's index length.
    Return: bool
    """
    if isinstance(indexs, int):
        indexs = [indexs]
    if length is None and _iterable:
        count = len(_iterable)
    else:
        count = length
    return not all(i < count if i > 0 else i >= -count for i in indexs)

# encoding

class encoding:
    GBK  = "gbk"
    UTF8 = "utf-8"
    GB18030 = "gb18030"