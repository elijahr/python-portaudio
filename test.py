#!/usr/bin/env python

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
