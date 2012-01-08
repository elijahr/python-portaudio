#!/usr/bin/env python

import sys
import os

# was necessary for python3
sys.path.append(os.path.join(os.path.dirname(__file__), 'portaudio'))

from portaudio import PortAudio
from portaudio.stream import Stream
from ctypes import c_float
from math import pi, sin
from time import sleep


with PortAudio():

    NUM_SECONDS = 1
    SAMPLE_RATE = 44100
    FRAMES_PER_BUFFER = 10240
    TABLE_SIZE = 200
    CHANNELS = 2

    stream = Stream(sample_rate=SAMPLE_RATE, frames_per_buffer=FRAMES_PER_BUFFER,
                    channel_count=CHANNELS)

    stream.open()
    buff = ((c_float * CHANNELS) * FRAMES_PER_BUFFER)()
    # initialise sinusoidal wavetable
    sine_constructor = (c_float * TABLE_SIZE)
    values = [c_float(sin(( float(i)/TABLE_SIZE ) * pi * 2. )) for i in range(TABLE_SIZE) ]
    sine = sine_constructor(*values)

    left_phase = 0
    right_phase = 0
    left_inc = 1
    right_inc = 4

    buffer_count = int(((NUM_SECONDS * SAMPLE_RATE) / FRAMES_PER_BUFFER))
    while True:
        for k in range(3):
            stream.start()
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

                stream.write(buff, FRAMES_PER_BUFFER)
            stream.stop()

            left_inc += 1
            right_inc += 1

    stream.close()
