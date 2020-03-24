import asyncio
import contextlib
import faulthandler

import numpy as np
import pytest
import soundfile as sf
import uvloop

faulthandler.enable(all_threads=True)

from portaudio import Stream, Output, Input

try:
    import tracemalloc
    tracemalloc.start()
except ImportError:
    # Not available in pypy
    ...


DTYPE = 'f'

WAVE_MONO, RATE = sf.read('count_to_10_mono.ogg')
WAVE_MONO = np.ascontiguousarray(WAVE_MONO.astype('f').T[0])

WAVE_STEREO, _RATE = sf.read('count_to_10_stereo.ogg')
WAVE_STEREO = WAVE_STEREO.astype('f')

# sanity check
assert _RATE == RATE


STREAM_INPUT = Stream(sample_rate=RATE, config=Input(format=DTYPE, channels=1))
STREAM_OUTPUT_MONO = Stream(sample_rate=RATE, config=Output(format=DTYPE, channels=1))
STREAM_OUTPUT_STEREO = Stream(sample_rate=RATE, interleaved=False, config=Output(format=DTYPE, channels=2))
STREAM_OUTPUT_STEREO_INTERLEAVED = Stream(sample_rate=RATE, interleaved=False, config=Output(format=DTYPE, channels=2))
STREAM_DUPLEX_MONO = Stream(sample_rate=RATE, config=(
    Input(format=DTYPE, channels=1),
    Output(format=DTYPE, channels=1)))
STREAM_DUPLEX_STEREO = Stream(sample_rate=RATE, interleaved=False, config=(
    Input(format=DTYPE, channels=1),
    Output(format=DTYPE, channels=2)))
STREAM_DUPLEX_STEREO_INTERLEAVED = Stream(sample_rate=RATE, interleaved=True, config=(
    Input(format=DTYPE, channels=1),
    Output(format=DTYPE, channels=2)))


@pytest.fixture(params=(
    STREAM_INPUT,
    STREAM_DUPLEX_MONO,
))
def input_stream(request):
    stream = request.param
    try:
        stream.start()
        yield stream
    finally:
        if stream.running:
            stream.stop()


@pytest.fixture(params=(
    STREAM_OUTPUT_MONO,
    STREAM_OUTPUT_STEREO,
    STREAM_DUPLEX_MONO,
    STREAM_DUPLEX_STEREO,
))
def output_stream(request):
    stream = request.param
    try:
        stream.start()
        yield stream
    finally:
        stream.stop()


@pytest.fixture(autouse=True, params=[
    # asyncio,
    uvloop
])
def event_loop(request):
    loop_mod = request.param
    loop = loop_mod.new_event_loop()
    asyncio.set_event_loop(loop)
    if loop_mod != uvloop:
        # uvloop in debug mode calls extract_stack, which results in "ValueError: call stack is not deep enough"
        # for Cython code
        loop.set_debug(True)
    with contextlib.closing(loop):
        yield loop


@pytest.mark.asyncio
async def test_stream_write(output_stream: Stream):
    assert output_stream.output_capacity > 0
    assert output_stream.output_read_available == 0
    assert output_stream.output_write_available == output_stream.output_capacity
    if output_stream.config[1].channels == 1:
        await output_stream.write(WAVE_MONO)
    else:
        await output_stream.write(WAVE_STEREO)
    assert output_stream.output_read_available == 0
    assert output_stream.output_write_available == output_stream.output_capacity


@pytest.mark.asyncio
async def test_stream_read(input_stream: Stream):
    assert input_stream.input_capacity > 0
    assert input_stream.input_read_available == 0
    assert input_stream.input_write_available == input_stream.input_capacity
    recording = await input_stream.read(44100)
    assert len(recording) == 44100

