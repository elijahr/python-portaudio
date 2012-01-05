#!/usr/bin/env python

from portaudio.stream import *

stream = Stream()
stream.open()
stream.write('asdlkjasdlkajsdlkajasdlkjasldk')
stream.close()

with Stream() as stream:
    stream.write('asdlkjasdlkajsdlkajasdlkjasldk')
