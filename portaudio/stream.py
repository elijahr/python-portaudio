
from portaudio.exceptions import get_exception, NoError
from portaudio import flags

from ctypes import *
from portaudio import _portaudio

try:
    raise get_exception(_portaudio.Pa_Initialize())
except NoError:
    pass


#output_parameters = pa.PaStreamParameters()
#output_parameters.device = pa.Pa_GetDefaultOutputDevice()

#if output_parameters.device == pa.paNoDevice:
#    raise Exception('Error: no default output device')


#output_parameters.channelCount = 2
#output_parameters.sampleFormat = pa.paFloat32
#infoPointer = pa.Pa_GetDeviceInfo( output_parameters.device )
#output_parameters.suggestedLatency = infoPointer.contents.defaultLowOutputLatency
#output_parameters.hostApiSpecificStreamInfo = None

#data = paTestData()
#stream = c_void_p(pa.PaStream)

#err = pa.Pa_OpenStream(
#          stream,
#          None,
#          output_parameters,
#          SAMPLE_RATE,
#          FRAMES_PER_BUFFER,
#          pa.paClipOff,
#          pa.PaStreamCallback(patestCallback),
#          data );


def get_default_output_parameters():
    output_parameters = _portaudio.PaStreamParameters()
    output_parameters.device = _portaudio.Pa_GetDefaultOutputDevice()
    info = _portaudio.Pa_GetDeviceInfo(output_parameters.device)
    output_parameters.channelCount = max(info.contents.maxOutputChannels, 2)
    output_parameters.sampleFormat = _portaudio.paFloat32
    device_info = _portaudio.Pa_GetDeviceInfo( output_parameters.device )
    output_parameters.suggestedLatency = device_info.contents.defaultLowOutputLatency
    output_parameters.hostApiSpecificStreamInfo = None
    return output_parameters


class Stream(object):

    def __init__(self, output_parameters=None, sample_rate=44100,
                 frames_per_buffer=64, flags=flags.CLIPOFF):

        self.sample_rate = c_double(sample_rate)
        self.frames_per_buffer = c_ulong(frames_per_buffer)
        self.in_stream = POINTER(c_void_p)()
        self.out_stream = POINTER(c_void_p)()
        self.data = POINTER(c_void_p)()
        self.flags = flags
        if output_parameters:
            self.output_parameters = output_parameters
        else:
            # build some default parameters
            self.output_parameters = get_default_output_parameters()


    def open(self):

        def _callback(*args, **kwargs):
            return 0

        # First argument to CFUNCTYPE is the return type:
        callback = _portaudio.PaStreamCallback(_callback)

        err = _portaudio.Pa_OpenStream(byref(self.out_stream),
                                byref(self.in_stream),
                                byref(self.output_parameters),
                                self.sample_rate,
                                self.frames_per_buffer,
                                self.flags,
                                byref(callback),
                                byref(self.data))

        try:
            raise get_exception(err)
        except NoError:
            pass

    def callback(self):
        print 'in callback'

    def read(self, size):
        pass
    def write(self, bytes):
        pass
    def close(self):
        pass
