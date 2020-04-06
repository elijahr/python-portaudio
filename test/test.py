import asyncio
import contextlib
import faulthandler
import os
import sys

import numpy as np
import pytest
import soundfile
import uvloop

faulthandler.enable(all_threads=True)

import pdb; pdb.set_trace()

from portaudio import Stream, Output, Input, FRAMES_PER_BUFFER_UNSPECIFIED, FLOAT32, INT32

try:
    import tracemalloc

    tracemalloc.start()
except ImportError:
    # Not available in pypy
    ...

WAVE_MONO, RATE = soundfile.read(os.path.join(os.path.dirname(__file__), 'count_to_10_mono.ogg'))
WAVE_MONO = np.ascontiguousarray(WAVE_MONO.astype('f').T[0])[:128]

WAVE_STEREO, _RATE = soundfile.read(os.path.join(os.path.dirname(__file__), 'count_to_10_stereo.ogg'))
WAVE_STEREO = WAVE_STEREO.astype('f')[:128]

# sanity check
assert _RATE == RATE


@pytest.fixture(params=(True, False))
def is_duplex(request):
    return request.param


@pytest.fixture(params=(True, False))
def is_stereo(request):
    return request.param


@pytest.fixture(params=(FRAMES_PER_BUFFER_UNSPECIFIED, 44100))
def frames_per_buffer(request):
    return request.param


@pytest.fixture(params=(True, False))
def interleaved(request):
    return request.param


@pytest.fixture(params=(True, False))
def clip(request):
    return request.param


@pytest.fixture(params=(True, False))
def dither(request):
    return request.param


@pytest.fixture(params=(True, False))
def prime_output_buffers(request, frames_per_buffer):
    return request.param


@pytest.fixture(params=(True, False))
def never_drop_input_input_stream(request, is_duplex, frames_per_buffer):
    if is_duplex and frames_per_buffer == FRAMES_PER_BUFFER_UNSPECIFIED and sys.platform != 'darwin':
        # It seems there is a bug in PortAudio's CoreAudio implementation whereby never_drop_input doesn't work,
        # so just skip those tests for now
        return request.param
    return False


@pytest.fixture(params=(True, False))
def never_drop_input_output_stream(request, is_duplex, frames_per_buffer):
    if is_duplex and frames_per_buffer == FRAMES_PER_BUFFER_UNSPECIFIED and sys.platform != 'darwin':
        # It seems there is a bug in PortAudio's CoreAudio implementation whereby never_drop_input doesn't work,
        # so just skip those tests for now
        return request.param
    return False


@pytest.fixture
def input_stream(
        is_duplex, is_stereo, frames_per_buffer, interleaved, clip, dither, prime_output_buffers,
        never_drop_input_input_stream):
    if is_duplex:
        config = (Input(format='f', channels=1), Output(format='f', channels=2 if is_stereo else 1,
                                                        interleaved=interleaved if is_stereo else False))
    else:
        config = Input(format='f', channels=1)
    stream = Stream(
        config=config,
        sample_rate=RATE,
        frames_per_buffer=frames_per_buffer,
        clip=clip,
        dither=dither,
        prime_output_buffers=prime_output_buffers,
        never_drop_input=never_drop_input_input_stream
    )
    try:
        stream.start()
        yield stream
    finally:
        if stream.running:
            stream.stop()


@pytest.fixture
def output_stream(
        is_duplex, is_stereo, frames_per_buffer, interleaved, clip, dither, prime_output_buffers,
        never_drop_input_output_stream):
    if is_duplex:
        config = (Input(format='f', channels=1), Output(format='f', channels=2 if is_stereo else 1,
                                                        interleaved=interleaved if is_stereo else False))
    else:
        config = Output(format='f', channels=2 if is_stereo else 1)
    stream = Stream(
        config=config,
        sample_rate=RATE,
        frames_per_buffer=frames_per_buffer,
        clip=clip,
        dither=dither,
        prime_output_buffers=prime_output_buffers,
        never_drop_input=never_drop_input_output_stream
    )
    try:
        stream.start()
        yield stream
    finally:
        if stream.running:
            stream.stop()
            from time import sleep
            sleep(5)


@pytest.fixture
def null_duplex_stream(
        is_stereo, frames_per_buffer, interleaved, clip, dither,
        prime_output_buffers, never_drop_input_output_stream):
    config = (Input(format='f', channels=1), Output(format='f', channels=2 if is_stereo else 1,
                                                    interleaved=interleaved if is_stereo else False))
    stream = Stream(
        config=config,
        sample_rate=RATE,
        frames_per_buffer=frames_per_buffer,
        clip=clip,
        dither=dither,
        prime_output_buffers=prime_output_buffers,
        never_drop_input=never_drop_input_output_stream,
        null=True,
    )
    try:
        stream.start()
        yield stream
    finally:
        if stream.running:
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


def test_config_flags(interleaved):
    config = Output(format='f', channels=2, interleaved=interleaved)
    assert config.format == FLOAT32
    assert config.interleaved == interleaved
    config.interleaved = not interleaved
    assert config.format == FLOAT32
    assert config.interleaved != interleaved
    config.interleaved = True
    config.format = INT32
    assert config.interleaved
    config.interleaved = False
    assert config.format == INT32
    assert not config.interleaved


@pytest.mark.asyncio
async def test_stream_write(output_stream: Stream):
    assert output_stream.output_capacity > 0
    assert output_stream.output_read_available == 0
    assert output_stream.output_write_available == output_stream.output_capacity
    if output_stream.config[1].channels == 1:
        wave = WAVE_MONO
    else:
        wave = WAVE_STEREO
    if not output_stream.config[1].interleaved:
        wave = wave.T
    await output_stream.write(wave)
    assert output_stream.output_read_available == 0
    assert output_stream.output_write_available == output_stream.output_capacity


@pytest.mark.asyncio
async def test_stream_read(input_stream: Stream):
    assert input_stream.input_capacity > 0
    assert input_stream.input_read_available == 0
    assert input_stream.input_write_available == input_stream.input_capacity
    recording = await input_stream.read(input_stream.input_capacity)
    assert len(recording) == input_stream.input_capacity


def test_stream_flags(is_duplex, frames_per_buffer):
    if is_duplex:
        config = (Input(format='f', channels=1), Output(format='f', channels=1))
    else:
        config = Output(format='f', channels=1)
    stream = Stream(
        sample_rate=RATE,
        frames_per_buffer=frames_per_buffer,
        config=config)
    assert stream.flags == 0
    never_drop_input = stream.is_duplex \
                       and stream.frames_per_buffer == FRAMES_PER_BUFFER_UNSPECIFIED \
                       and sys.platform != 'darwin'
    assert stream.clip
    assert stream.dither
    assert stream.never_drop_input == never_drop_input
    assert not stream.prime_output_buffers
    stream.clip = False
    assert not stream.clip
    assert stream.dither
    assert stream.never_drop_input == never_drop_input
    assert not stream.prime_output_buffers
    stream.dither = False
    assert not stream.clip
    assert not stream.dither
    assert stream.never_drop_input == never_drop_input
    assert not stream.prime_output_buffers
    stream.never_drop_input = not never_drop_input
    assert not stream.clip
    assert not stream.dither
    assert stream.never_drop_input != never_drop_input
    assert not stream.prime_output_buffers
    stream.prime_output_buffers = True
    assert not stream.clip
    assert not stream.dither
    assert stream.never_drop_input != never_drop_input
    assert stream.prime_output_buffers


@pytest.mark.asyncio
def test_integrity(null_duplex_stream):
    pass
