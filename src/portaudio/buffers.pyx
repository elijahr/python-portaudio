import struct
from contextlib import contextmanager
from math import log, ceil
from typing import Iterator

try:
    import numpy as np
except ImportError:
    np = None

from libc.limits cimport CHAR_MIN as _CHAR_MIN, CHAR_MAX as _CHAR_MAX, SCHAR_MIN as _SCHAR_MIN, \
    SCHAR_MAX as _SCHAR_MAX, UCHAR_MAX as _UCHAR_MAX, SHRT_MIN as _SHRT_MIN, SHRT_MAX as _SHRT_MAX, \
    USHRT_MAX as _USHRT_MAX, INT_MIN as _INT_MIN, INT_MAX as _INT_MAX, UINT_MAX as _UINT_MAX, LONG_MIN as _LONG_MIN, \
    LONG_MAX as _LONG_MAX, ULONG_MAX as _ULONG_MAX, LLONG_MIN as _LLONG_MIN, LLONG_MAX as _LLONG_MAX, \
    ULLONG_MAX as _ULLONG_MAX
from libc.float cimport FLT_MIN as _FLT_MIN, FLT_MAX as _FLT_MAX, DBL_MIN as _DBL_MIN, DBL_MAX as _DBL_MAX

from cython.view cimport array as _Array

from . import exceptions, formats


__all__ = ['AudioBuffer', 'Array']


CHAR_MIN = _CHAR_MIN
CHAR_MAX = _CHAR_MAX
SCHAR_MIN = _SCHAR_MIN
SCHAR_MAX = _SCHAR_MAX
UCHAR_MAX = _UCHAR_MAX
SHRT_MIN = _SHRT_MIN
SHRT_MAX = _SHRT_MAX
USHRT_MAX = _USHRT_MAX
INT_MIN = _INT_MIN
INT_MAX = _INT_MAX
UINT_MAX = _UINT_MAX
LONG_MIN = _LONG_MIN
LONG_MAX = _LONG_MAX
ULONG_MAX = _ULONG_MAX
LLONG_MIN = _LLONG_MIN
LLONG_MAX = _LLONG_MAX
ULLONG_MAX = _ULLONG_MAX
FLT_MIN = _FLT_MIN
FLT_MAX = _FLT_MAX
DBL_MIN = _DBL_MIN
DBL_MAX = _DBL_MAX


class Array(_Array):

    if np:
        def __setitem__(self, item, value):
            # Sanity checks to prevent segfaults with invalid data
            if isinstance(value, np.ndarray):
                try:
                    assert formats.DTYPE_FORMAT[value.dtype] == (<_Array>self).format
                except (AssertionError, KeyError):
                    msg = 'Invalid numpy %r for %r' % (value.dtype, (<_Array>self).format)
                    if (<_Array>self).struct_format in formats.FORMAT_DTYPE:
                        msg += ', expected %r' % formats.FORMAT_DTYPE[(<_Array>self).format]
                    raise TypeError(msg)
            self.memview[item] = value


cdef class AudioBuffer:

    def __cinit__(self, struct_format: str, *, channels: int, interleaved: bool, size: int):
        if channels < 1:
            raise ValueError('Invalid number of channels: %r must be >= 1' % channels)
        if size <= 0:
            raise ValueError('Invalid size %r' % size)
        # Make size a power of two
        print('SIZE IS ', size)
        size = pow(2, ceil(log(size)/log(2)))
        self.struct_format = struct_format
        self.channels = channels
        self.interleaved = interleaved
        # self.size = size
        self.itemsize = struct.calcsize(self.struct_format)
        self.bip = bb_create(size * self.itemsize)
        if self.bip is NULL:
            raise MemoryError
        self._shapes = {}

    def __init__(self, struct_format: str, *, channels: int, interleaved: bool, size: int):
        pass

    def __dealloc__(self):
        bb_destroy(self.bip)

    def __repr__(self):
        return '%s(%r, channels=%r, interleaved=%r, size=%r)' % (
            self.__class__.__name__, self.struct_format, self.channels, self.interleaved, self.size)

    def clear(self):
        bb_clear(self.bip)

    @property
    def size(self) -> int:
        return int(self.bip.size / self.itemsize)

    @property
    def allocated(self) -> int:
        return int(self.bip.allocated / self.itemsize)

    @contextmanager
    def allocate(self, size: int, block: bool = True) -> Iterator[memoryview]:
        cdef:
            long int bytesize = size * self.itemsize
            void *data = NULL
            int ret
            bint blk = block
            _Array arr

        import uuid
        id = str(uuid.uuid4())
        print("bb_alloc for %s, size %r, " % (id, size))
        with nogil:
            data = bb_alloc(self.bip, bytesize, blk)

        foo = data is NULL
        print("bb_alloc'd for %s, self.bip.allocated=%r, is null? %r" % (id, self.bip.allocated, foo))
        if data is NULL:
            raise exceptions.BufferOverflow('Could not allocate %r bytes' % bytesize)

        arr = _Array(
            format=self.struct_format,
            shape=self._get_shape(size),
            mode='c',
            itemsize=self.itemsize,
            allocate_buffer=False)
        arr.data = <char*>data

        try:
            yield arr
        except:
            print("bb_clear for %s" % id)
            with nogil:
                bb_clear(self.bip)
            raise
        finally:
            del arr

        print("bb_commit for %s" % id)
        with nogil:
            ret = bb_commit(self.bip, bytesize)

        if ret == ERR_COMMIT_MISMATCH:
            raise exceptions.CommitMismatch('Could not commit %r bytes (%r allocated)' % (bytesize, self.bip.allocated))

    def read(self, size: int, block: bool = True) -> memoryview:
        cdef:
            long int bytesize = size * self.itemsize
            long int read_bytes
            bint blk = block
            _Array arr

        arr = _Array(
            format=self.struct_format,
            shape=self._get_shape(size),
            mode='c',
            itemsize=self.itemsize,
            allocate_buffer=True)

        with nogil:
            read_bytes = bb_read(self.bip, <char*>arr.data, bytesize, blk)

        if read_bytes == ERR_UNDERFLOW:
            del arr
            raise exceptions.BufferUnderflow

        return arr

    def look(self, size: int) -> memoryview:
        cdef:
            long int bytesize = size * self.itemsize
            long int read_bytes

        arr = Array(
            format=self.struct_format,
            shape=self._get_shape(size),
            mode='c',
            itemsize=self.itemsize,
            allocate_buffer=True)

        with nogil:
            read_bytes = bb_look(self.bip, <char*>(<_Array>arr).data, bytesize)

        if read_bytes == ERR_UNDERFLOW:
            del arr
            raise exceptions.BufferUnderflow

        return arr

    # def look(self, size: int) -> memoryview:
    #     cdef:
    #         long int bytesize = size * self.itemsize
    #         long int read_bytes
    #         long int read_samples
    #         char* data = <char*>malloc(bytesize)
    #         tuple shape
    #         tuple strides
    #
    #     with nogil:
    #         read_bytes = bb_look(self.bip, data, bytesize)
    #
    #     if read_bytes <= 0:
    #         raise BufferUnderflow('Read %r bytes' % read_bytes)
    #
    #     read_samples = int(read_bytes / self.itemsize)
    #
    #     # stride[0] is the distance between the first elements of adjacent channels.
    #     # stride[1] is the distance, in bytes, between two samples in the same channel.
    #     # if self.interleaved:
    #     #     #                                                     strides[0]
    #     #     #                                                    /¯\
    #     #     # If (stereo) data is interleaved, it's of the form [L, R, L, R, L, R]
    #     #     #                                                    \____/
    #     #     #                                                     strides[1]
    #     #     #
    #     #     strides = (
    #     #         self.itemsize,
    #     #         self.itemsize * self.channels)
    #     # else:
    #     #     #                                                         strides[1]
    #     #     #                                                        /¯¯¯¯¯¯¯\
    #     #     # If (stereo) data is not interleaved, it's of the form [L, L, L, R, R, R]
    #     #     #                                                        \_/
    #     #     #                                                         strides[0]
    #     #     strides = (
    #     #         self.itemsize * self.size,
    #     #         int(read_samples / self.channels))
    #     #     shape =
    #         # shape[0] is the number of samples per channel
    #         # shape[1] is the number of samples, total
    #
    #     print('look, read_samples is', read_samples)
    #     print('look, shape is', self._get_shape(read_samples))
    #     arr = <cy_array>cy_array(
    #         format=self.struct_format,
    #         shape=self._get_shape(read_samples),
    #         mode='c',
    #         itemsize=self.itemsize,
    #         allocate_buffer=False)
    #     arr.data = data
    #     arr.callback_free_data = free
    #
    #     return arr

    cdef tuple _get_shape(AudioBuffer self, unsigned long int samples):
        cdef tuple shape
        try:
            # Use cached shape, to avoid unnecessary re-allocation/de-allocation of tuples
            shape = self._shapes[samples]
        except KeyError:
            if self.interleaved:
                shape = (samples, )
            else:
                shape = (self.channels, int(samples / self.channels))
            self._shapes[samples] = shape
        return shape

