import array
import contextlib
from typing import Union, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from . import buffers


from . import asyncio_helpers


def truncate_repr(arr: array.array):
    r = repr(arr)
    if len(arr) > 10:
        r = r[:12] + ', '.join((list(map(repr, arr[:3])) + ['...'] + list(map(repr, arr[-3:])))) + r[-2:]
    return r


class GiveFuture(asyncio_helpers.ThreadSafeFuture):
    __slots__ = ('data', 'timeout')

    data: array.array
    timeout: float

    def __init__(self, *, data: Union[array.array, None], timeout: Union[int, float] = -1, **kwargs):
        self.data = data
        self.timeout = timeout
        super(GiveFuture, self).__init__(**kwargs)

    def __repr__(self):
        parts = ['data=%s' % truncate_repr(self.data)]
        if self.timeout >= 0:
            parts.append('timeout=%r' % self.timeout)
        elif self.timeout == -1:
            parts.append('timeout=WAIT')
        return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))


class TakeFuture(asyncio_helpers.ThreadSafeFuture):
    __slots__ = ('take', 'timeout')

    take: int
    timeout: float

    def __repr__(self):
        parts = ['take=%s' % 'TAKE_ALL' if self.take == -1 else self.take]
        if self.timeout >= 0:
            parts.append('timeout=%r' % self.timeout)
        elif self.timeout == -1:
            parts.append('timeout=WAIT')
        return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))

    def __init__(self, *, take: int = -1, timeout: Union[int, float] = -1, **kwargs):
        self.take = take
        self.timeout = float(timeout)
        super(TakeFuture, self).__init__(**kwargs)


@contextlib.asynccontextmanager
async def buffer_fill(
        self: 'buffers.AudioBuffer',
        take: int = -1,
        timeout: Union[int, float] = -1
) -> Tuple[int, array.array]:
    """
    A context manager that upon enter will wake up any pending producers and consume.

    :param self: The Buffer instance.
    :param take: The number of samples to fill.
                 If -1 (the default), the buffer will fill with whatever data is available, or block until data is
                 available.
                 Otherwise, the function will block until that number of samples is produced.
    :param timeout: The number of seconds to block before underflowing.
    :return: None
    """
    take_fut = TakeFuture(take=take, timeout=timeout)
    # print('buffer_fill: %r' % take_fut)
    self.take_queue.put(take_fut)
    data = await take_fut
    # print('buffer_fill: %s' % truncate_repr(data))
    self.data[:] = data
    yield data


@contextlib.asynccontextmanager
async def buffer_flush(
        self: 'buffers.AudioBuffer',
        timeout: Union[int, float] = -1
) -> int:
    """
    A context manager that upon exit will allocate the buffer's data and wake up any consumers.

    :param self: The Buffer instance.
    :param timeout: The number of seconds to block before overflowing.
    :return: an error code, either BUFFER_NO_ERROR, or BUFFER_OVERLFOW
    """
    give_fut = GiveFuture(data=None, timeout=timeout)
    yield give_fut

    # After context closes, copy buffer data to the futurex
    give_fut.data = self.data[:]

    # Clear the buffer
    self.data[:] = array.array(self.format)

    # Put the future in the queue and wait for the result
    # print('buffer_flush: %r' % give_fut)
    self.give_queue.put(give_fut)
    await give_fut
