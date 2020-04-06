import asyncio
from functools import reduce
from operator import mul

from typing import TYPE_CHECKING, Any, Union
from ringbuf import Array, concatenate

from . import exceptions, pa

try:
    import numpy as np
except ImportError:
    np = None

if TYPE_CHECKING:
    from . import streams


async def stream_read(
        self: 'streams.Stream',
        count: int,
        spin_wait: Union[int, float] = 0) -> Union[Array, None]:
    if not self.running or self.stopping:
        exceptions.check_error(pa.STREAM_IS_STOPPED)

    if not self.is_input:
        exceptions.check_error(pa.CAN_NOT_READ_FROM_AN_OUTPUT_ONLY_STREAM)

    buffer = self.buffer[0]
    parts = []
    count *= self.config[0].channels
    total = 0
    while True:
        # spin until all requested data has been popped, or timeout
        popped = buffer.pop(count - total)
        if popped is not None:
            total += len(popped)
            parts.append(popped)
        if total < count:
            await asyncio.sleep(spin_wait)
            if not self.running or self.stopping:
                exceptions.check_error(pa.STREAM_IS_STOPPED)
        else:
            break

    if len(parts) == 1:
        return parts[0]
    elif len(parts):
        return concatenate(*parts)
    return None


async def stream_write(
        self: 'streams.Stream',
        data: Any,
        spin_wait: Union[int, float] = 0) -> None:

    if not self.running or self.stopping:
        exceptions.check_error(pa.STREAM_IS_STOPPED)

    if not self.is_output:
        exceptions.check_error(pa.CAN_NOT_WRITE_TO_AN_INPUT_ONLY_STREAM)

    buffer = self.buffer[1]
    remaining = unshape(data, interleaved=self.config[1].interleaved)

    while True:
        # spin until all data has been pushed
        remaining = buffer.push(remaining)
        if remaining is not None:
            await asyncio.sleep(spin_wait)
            if not self.running:
                exceptions.check_error(pa.STREAM_IS_STOPPED)
        else:
            break

    while self.output_read_available > 0:
        # spin until all data has been consumed or stream is stopped
        await asyncio.sleep(spin_wait)
        if not self.running or self.stopping:
            exceptions.check_error(pa.STREAM_IS_STOPPED)


def unshape(data: Any, interleaved: bool) -> Any:
    memview = memoryview(data)
    try:
        if memview.ndim > 1:
            if np is None:
                raise ValueError('Only 1-dimensional buffers are supported without numpy')
            else:
                # Reshape, since ringbuf only accepts 1-d data
                shape = (reduce(mul, memview.shape, 1),)
                data = np.array(memview, dtype=memview.format)
                if not interleaved:
                    data = data.T
                data = data.reshape(shape)
                data = np.ascontiguousarray(data)
    finally:
        memview.release()

    return data
