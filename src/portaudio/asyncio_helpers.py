import asyncio
from typing import Any


class ThreadSafeFuture(asyncio.Future):

    def set_result(self, result: Any) -> None:
        self._loop.call_soon_threadsafe(super(ThreadSafeFuture, self).set_result, result)

    def set_exception(self, exception: BaseException) -> None:
        self._loop.call_soon_threadsafe(super(ThreadSafeFuture, self).set_exception, exception)

