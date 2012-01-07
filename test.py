#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'portaudio'))

from portaudio.stream import *

with PortAudio():
    stream = Stream()
    stream.open()
    stream.start()
    stream.write('asdlkjasdlkajsdlkajasdlkjasldk')
    stream.stop()
    stream.close()

with PortAudio():
    with Stream() as stream:
        stream.write('asdlkjasdlkajsdlkajasdlkjasldk')
