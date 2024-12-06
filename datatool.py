class mutli_value():
    """A list that can be calculated.
    Recommend to use numpy.ndarray"""
    def __init__(self, *values_not_list) -> None:
        self.values = [*values_not_list]
        self.legth = self.values.__len__()
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return mutli_value(*[i+other for i in self.values])
        return mutli_value(*[i+j for i,j in zip(self.values, other.values)])
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return mutli_value(*[i-other for i in self.values])
        return mutli_value(*[i-j for i,j in zip(self.values, other.values)])
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return mutli_value(*[i/other for i in self.values])
        return mutli_value(*[i/j for i,j in zip(self.values, other.values)])
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return mutli_value(*[i*other for i in self.values])
        return mutli_value(*[i*j for i,j in zip(self.values, other.values)])
    def __lt__(self, value, /):
        if isinstance(value, (int, float)):
            return [i<value for i in self.values]
        elif isinstance(value, mutli_value):
            return [i<j for i,j in zip(self.values, value.values)]
        else:
            return [i<j for i,j in zip(self.values, value)]
    def __le__(self, value, /):
        if isinstance(value, (int, float)):
            return [i<=value for i in self.values]
        elif isinstance(value, mutli_value):
            return [i<=j for i,j in zip(self.values, value.values)]
        else:
            return [i<=j for i,j in zip(self.values, value)]
    def __gt__(self, value, /):
        if isinstance(value, (int, float)):
            return [i>value for i in self.values]
        elif isinstance(value, mutli_value):
            return [i>j for i,j in zip(self.values, value.values)]
        else:
            return [i>j for i,j in zip(self.values, value)]
    def __ge__(self, value, /):
        if isinstance(value, (int, float)):
            return [i>=value for i in self.values]
        elif isinstance(value, mutli_value):
            return [i>=j for i,j in zip(self.values, value.values)]
        else:
            return [i>=j for i,j in zip(self.values, value)]
    def __eq__(self, value, /):
        '''
        self == list => [bool,...], self == int/float/double/... => [bool,...]
        '''
        # BUG: when value is list or iterable, it raise implicit 
        if isinstance(value, (int, float)):
            return [i==value for i in self.values]
        elif isinstance(value, mutli_value):
            return [i==j for i,j in zip(self.values, value.values)]
        else:
            return [i==j for i,j in zip(self.values, value)]
    def __abs__(self): return mutli_value(*[abs(i) for i in self.values])
    def __neg__(self): return mutli_value(*[-i for i in self.values])
    def __max__(self): return max(self.values)
    def __min__(self): return min(self.values)
    def __getitem__(self, index):
        if index < -self.legth or index >= self.legth:
            raise IndexError("Index out of range")
        return self.values[index]
    def __iter__(self): return iter(self.values)
    def __len__(self): return self.legth
    def __repr__(self): return str(self.values)
    def __format__(self, format_spec):
        if 'f' in format_spec:
            return ', '.join('{:{}}'.format(value, format_spec) for value in self.values)
        elif format_spec == '':
            return ', '.join(f'{value}' for value in self.values)
        else:
            raise ValueError(f'Unsupported format specifier: {format_spec}')

def encode_key(data):
    # HACK: return {1:"name1", 2:"name2", ...}
    return {i + 1: val for i, val in enumerate(data)}