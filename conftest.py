import asyncio
import contextlib
import glob
import itertools
import logging
import os

import pytest
import uvloop


try:
    import tracemalloc
    tracemalloc.start()
except ImportError:
    # Not available in pypy
    pass


# clear compiled cython tests
for path in itertools.chain(
        glob.glob(os.path.join('tests', '*.so')),
        glob.glob(os.path.join('tests', '*.c'))):
    os.unlink(path)


@pytest.fixture(params=[
    asyncio,
    uvloop
])
def loop_mod(request):
    return request.param


@pytest.fixture(autouse=True)
def foo():
    print('TEST IS', os.environ.get('PYTEST_CURRENT_TEST'))


def event_loop(loop_mod):
    loop = loop_mod.new_event_loop()
    asyncio.set_event_loop(loop)
    if loop_mod != uvloop:
        # uvloop in debug mode calls extract_stack, which results in "ValueError: call stack is not deep enough"
        # for Cython code
        loop.set_debug(True)
    with contextlib.closing(loop):
        yield loop


def pytest_configure(config):
    if config.getoption('verbose') > 0:
        h = logging.StreamHandler()
        h.setLevel(logging.DEBUG)
        logger = logging.getLogger('portaudio')
        logger.addHandler(h)
        logger.setLevel(logging.DEBUG)