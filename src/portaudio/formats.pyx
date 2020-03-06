from typing import Union

try:
    import numpy as np
except ImportError:
    np = None

from . import pa


__all__ = [
    'FORMAT_NAME', 'STRUCT_FORMAT', 'DTYPE_FORMAT', 'FORMAT_DTYPE',
]

if np:
    FormatType = Union[int, str, np.dtype]
    DTYPE_FORMAT = {
        np.dtype('byte'): 'b',
        np.dtype('ubyte'): 'B',

        np.dtype('int8'): 'b',
        np.dtype('uint8'): 'B',

        np.dtype('short'): 'h',
        np.dtype('ushort'): 'H',

        np.dtype('int16'): 'h',
        np.dtype('uint16'): 'H',

        np.dtype('intc'): 'i',
        np.dtype('uintc'): 'I',

        np.dtype('int_'): 'l',
        np.dtype('uint'): 'L',

        np.dtype('int32'): 'l',
        np.dtype('uint32'): 'L',

        np.dtype('longlong'): 'q',
        np.dtype('ulonglong'): 'Q',

        np.dtype('int64'): 'q',
        np.dtype('uint64'): 'Q',

        np.dtype('single'): 'f',
        np.dtype('double'): 'd',
    }
    FORMAT_DTYPE = {
        'b': np.dtype('byte'),
        'B': np.dtype('ubyte'),
        'h': np.dtype('short'),
        'H': np.dtype('ushort'),
        'i': np.dtype('intc'),
        'I': np.dtype('uintc'),
        'l': np.dtype('int_'),
        'L': np.dtype('uint'),
        'q': np.dtype('longlong'),
        'Q': np.dtype('ulonglong'),
        'f': np.dtype('single'),
        'd': np.dtype('double'),
    }
else:
    FormatType = Union[int, str]
    DTYPE_FORMAT = {}
    FORMAT_DTYPE = {}


FORMAT_NAME = {
    pa.FLOAT32: 'FLOAT32',
    pa.INT32: 'INT32',
    pa.INT24: 'INT24',
    pa.INT16: 'INT16',
    pa.INT8: 'INT8',
    pa.UINT8: 'UINT8',
}


STRUCT_FORMAT = {
    pa.FLOAT32: 'f',  # float
    pa.INT32: 'l',  # long
    pa.INT16: 'h',  # short
    pa.INT8: 'b',  # char
    pa.UINT8: 'B',  # unsigned char
}


SAMPLE_FORMATS = {
    'f': pa.FLOAT32,  # float
    'l': pa.INT32,  # long
    'h': pa.INT16,  # short
    'b': pa.INT8,  # char
    'B': pa.UINT8,  # unsigned char
}
