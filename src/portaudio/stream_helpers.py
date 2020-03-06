from collections.abc import AsyncIterator

from typing import TYPE_CHECKING, Tuple

from . import buffers

if TYPE_CHECKING:
    from . import streams


class AbstractStreamIterator(AsyncIterator):

    __slots__ = ('stream', )

    stream: 'streams.Stream'

    def __init__(self, stream: 'streams.Stream'):
        self.stream = stream


class DuplexStreamIterator(AbstractStreamIterator):

    async def __anext__(self) -> Tuple[buffers.AudioBuffer, buffers.AudioBuffer]:
        if not self.stream.active:
            self.stream.stop()
            raise StopAsyncIteration

        if not self.stream.running:
            raise StopAsyncIteration
        #
        # if self.stream.buffer[0].closed or self.stream.buffer[1].closed:
        #     raise StopAsyncIteration

        return self.stream.buffer[0], self.stream.buffer[1]


class InputStreamIterator(AbstractStreamIterator):

    async def __anext__(self) -> buffers.AudioBuffer:
        if not self.stream.active:
            self.stream.stop()
            raise StopAsyncIteration

        if not self.stream.running:
            raise StopAsyncIteration

        # if self.stream.buffer[0]:
        #     if self.stream.buffer[0].closed:
        #         raise StopAsyncIteration

        return self.stream.buffer[0]


class OutputStreamIterator(AbstractStreamIterator):

    async def __anext__(self) -> buffers.AudioBuffer:
        if not self.stream.active:
            self.stream.stop()
            raise StopAsyncIteration

        if not self.stream.running:
            raise StopAsyncIteration

        # if self.stream.buffer[1]:
        #     if self.stream.buffer[1].closed:
        #         raise StopAsyncIteration

        return self.stream.buffer[1]
