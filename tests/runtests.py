#!/usr/bin/env python

import ctypes
import os
import random
import sys
import time
import unittest


# was necessary for python3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'portaudio')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', )))


from portaudio import PortAudio, _portaudio
from portaudio.stream import Stream
from math import pi, sin


class PortAudioTest(unittest.TestCase):
    def test_blocking(self):
        with PortAudio():
            NUM_SECONDS = 0.25
            SAMPLE_RATE = 44100
            FRAMES_PER_BUFFER = 10240
            TABLE_SIZE = 200
            CHANNELS = 2

            out_stream = Stream(sample_rate=SAMPLE_RATE, frames_per_buffer=FRAMES_PER_BUFFER,
                                channel_count=CHANNELS)
            out_stream.open(mode='w')

            buff = ((ctypes.c_float * CHANNELS) * FRAMES_PER_BUFFER)()
            # initialise sinusoidal wavetable
            sine_constructor = (ctypes.c_float * TABLE_SIZE)
            values = [ctypes.c_float(sin(( float(i)/TABLE_SIZE ) * pi * 2. )) for i in range(TABLE_SIZE) ]
            sine = sine_constructor(*values)

            left_phase = 0
            right_phase = 0
            left_inc = 1
            right_inc = 4

            buffer_count = int(((NUM_SECONDS * SAMPLE_RATE) / FRAMES_PER_BUFFER))

            for k in range(10):
                out_stream.start()
                for i in range(buffer_count):
                    for j in range(FRAMES_PER_BUFFER):
                        buff[j][0] = sine[left_phase]
                        buff[j][1] = sine[right_phase]

                        left_phase += left_inc
                        if left_phase >= TABLE_SIZE:
                            left_phase -= TABLE_SIZE

                        right_phase += right_inc
                        if right_phase >= TABLE_SIZE:
                            right_phase -= TABLE_SIZE

                    out_stream.write(buff, FRAMES_PER_BUFFER)
                out_stream.stop()

                left_inc += 1
                right_inc += 1

            out_stream.close()

    def test_callback_stream(self):
        with PortAudio():

            SAMPLE_RATE = 44100
            CHANNELS = 2

            out_stream = Stream(sample_rate=SAMPLE_RATE, channel_count=CHANNELS)

            def callback(input, output, frame_count, time_info, status_flags, user_data):
                BufferArray = (ctypes.c_float * (frame_count*CHANNELS))
                buffer = BufferArray(*(ctypes.c_float(random.random()) for i in range(frame_count)))
                ctypes.memmove(output, buffer, frame_count*CHANNELS)
                return _portaudio.paContinue

            out_stream.open(mode='w', callback=callback, user_data=[])
            out_stream.start()

            for i in range(4):
                time.sleep(1)

            out_stream.stop()
            out_stream.close()

if __name__ == '__main__':
    unittest.main()