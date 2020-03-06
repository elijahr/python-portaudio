import asyncio
import contextlib
import faulthandler
import random
from time import sleep

import numpy as np
import pytest
import scipy.io.wavfile
import uvloop

faulthandler.enable(all_threads=True)

from portaudio import FLOAT32, Stream, Output

try:
    import tracemalloc
    tracemalloc.start()
except ImportError:
    # Not available in pypy
    ...

VOLUME = 0.5     # range [0.0, 1.0]
DURATION = 5.0   # in seconds, may be float
FREQ = 440.0        # sine frequency, Hz, may be float


# generate samples, note conversion to float32 array
def sine(duration, freq, rate=44100):
    return (np.sin(2 * np.pi * np.arange(rate * duration) * freq / rate)).astype(np.float32)


@pytest.fixture(autouse=True, params=[
    asyncio,
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
async def test_output():
    rate, waveform = scipy.io.wavfile.read('paris-dub-1.wav', mmap=False)
    waveform = np.ascontiguousarray(waveform.T[0])
    stream = Stream(sample_rate=rate, config=Output(format=waveform.dtype, channels=1))
    # waveform = sine(duration=0.2, freq=440)
    # for i in range(120):
    #     waveform = np.concatenate((waveform, sine(duration=0.2, freq=440 + random.randint(-220, 620))))

    i = 0
    step = 120
    async for buffer in stream:
        print(i, len(waveform), buffer.size)
        if i >= len(waveform):
            break
        chunked = waveform[i:i+step]
        print("BLOCKING")
        with buffer.allocate(len(chunked)) as chunk:
            print("WOKEUP")
            chunk[:] = chunked
            i += step

    sleep(10)

    stream.stop()
        # breakpoint()
        # buffer.fill(memoryview(waveform)[:len(buffer)])
        # await buffer.send(waveform)
        # buffer.stop()


#
# @pytest.mark.asyncio
# async def test_async_stream_duplex():
#     breakpoint()
#     in_config = Config(format=paFloat32, channels=1)
#     out_config = Config(format=paFloat32, channels=1)
#     stream = Stream(in_config=in_config, out_config=out_config, samples_per_buffer=44100)
#     stream.start()
#     recording = q_t(in_config, size=44100 * 4)
#     print('Recording 4 seconds of audio')
#     i = 0
#
#     async for pipe in stream:
#         recording += pipe.read()
#
#         pipe.write()

    #
    #     if i < recording.size:
    #         recording[i:i+44100] = in_buffer
    #         i += 44100
    #     else:
    #         await out_buffer.send()
    #
    #     # iterator should detect __anext__ call without outputting anything and just output silence automatically
    #     # await out_buffer.silence()
    #
    #     recorded_buffer += chunk
    #     print(len(recorded_buffer), stream.sample_rate * 5)
    #     if len(recorded_buffer) >= stream.sample_rate * 5:
    #         print('Stopping stream')
    #         await stream.stop()
    #         print("Stopped stream")
    # print('Recorded %s samples' % len(recorded_buffer))
    # print('Playing back recording')
    # out_config = Config(format=paFloat32, channels=1)
    # output_stream = Stream(out_config=out_config, samples_per_buffer=44100)
    # output_stream.start()
    # await output_stream.write(recorded_buffer)
    # await output_stream.stop()



