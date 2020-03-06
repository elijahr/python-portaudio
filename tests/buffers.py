import struct
from math import floor

import numpy as np
import pytest

from portaudio import AudioBuffer, BufferOverflow, BufferUnderflow, Array
from portaudio.buffers import SCHAR_MIN, SCHAR_MAX, UCHAR_MAX, SHRT_MIN, SHRT_MAX, USHRT_MAX, \
    INT_MIN, INT_MAX, UINT_MAX, LONG_MIN, LONG_MAX, ULONG_MAX, LLONG_MIN, LLONG_MAX, ULLONG_MAX, FLT_MIN, FLT_MAX, \
    DBL_MIN, DBL_MAX


def interleaved():
    for format, dtype, start, stop in (
            ('b', np.byte, SCHAR_MIN, SCHAR_MAX),
            ('B', np.ubyte, 0, UCHAR_MAX),
            ('h', np.short, SHRT_MIN, SHRT_MAX),
            ('H', np.ushort, 0, USHRT_MAX),
            ('i', np.intc, INT_MIN, INT_MAX),
            ('I', np.uintc, 0, UINT_MAX),
            ('l', np.int_, LONG_MIN, LONG_MAX),
            ('L', np.uint, 0, ULONG_MAX),
            ('q', np.longlong, LLONG_MIN, LLONG_MAX),
            ('Q', np.ulonglong, 0, ULLONG_MAX),
    ):

        data = np.linspace(start, stop, dtype=dtype)

        expected = Array(
            format=format,
            shape=(len(data),),
            mode='c',
            itemsize=struct.calcsize(format),
            allocate_buffer=True)

        expected[:] = data

        yield expected

    for format, dtype, start, stop in (
            ('f', np.single, FLT_MIN, FLT_MAX),
            ('d', np.double, DBL_MIN, DBL_MAX),
    ):
        data = np.linspace(start, stop, num=1024, dtype=dtype)

        expected = Array(
            format=format,
            shape=(len(data),),
            mode='c',
            itemsize=struct.calcsize(format),
            allocate_buffer=True)

        expected[:] = data

        yield expected


@pytest.mark.parametrize('expected', tuple(interleaved()))
@pytest.mark.parametrize('channels', (1, 2))
@pytest.mark.asyncio
async def test_audio_buffer_interleaved(channels, expected):
    size = len(expected)
    buffer = AudioBuffer(format=memoryview(expected).format, channels=channels, interleaved=True, size=size)

    assert buffer.size >= size
    assert buffer.allocated == 0
    with pytest.raises(BufferUnderflow):
        buffer.read(1)

    chunk = floor(size / 2)

    assert buffer.allocated == 0
    with buffer.allocate(chunk) as data:
        assert buffer.allocated == chunk
        assert data.shape == (chunk,)

        data[:] = expected[:chunk]

    assert buffer.allocated == 0
    with buffer.allocate(chunk) as data:
        assert buffer.allocated == chunk
        assert data.shape == (chunk,)

        data[:] = expected[chunk:chunk * 2]

    chunk = floor(size / 3)
    assert np.array_equal(np.array(buffer.look(size)), np.array(expected))
    assert np.array_equal(np.array(buffer.read(chunk)), np.array(expected[:chunk]))
    assert np.array_equal(np.array(buffer.read(chunk)), np.array(expected[chunk:chunk * 2]))
    assert np.array_equal(np.array(buffer.read(chunk)), np.array(expected[chunk * 2:chunk * 3]))

    with pytest.raises(BufferOverflow):
        toomuch = size + 10000
        with buffer.allocate(toomuch):
            ...
