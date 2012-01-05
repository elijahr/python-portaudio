
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



class Stream(object):

    def __init__(self, sample_rate=44100, frames_per_buffer=64, flags=flags.CLIPOFF):
        self._output_parameters = None
        self.sample_rate = c_double(sample_rate)
        self.frames_per_buffer = c_ulong(frames_per_buffer)
        self.stream = POINTER(c_void_p)()
        self.data = POINTER(c_void_p)()
        self.flags = flags

    @property
    def output_parameters(self):
        if not self._output_parameters:
            output_parameters = _portaudio.PaStreamParameters()
            output_parameters.device = _portaudio.Pa_GetDefaultOutputDevice()
            output_parameters.channelCount = c_int(2)
            output_parameters.sampleFormat = _portaudio.paFloat32
            device_info = _portaudio.Pa_GetDeviceInfo( output_parameters.device )
            output_parameters.suggestedLatency = device_info.contents.defaultLowOutputLatency
            output_parameters.hostApiSpecificStreamInfo = None
            self._output_parameters = output_parameters
        return self._output_parameters

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        print type, value, traceback
        print '-----------------'
        if type is None:
            self.close()
        else:
            raise value

    def open(self):

        def _callback(*args, **kwargs):
            print 'in _callback'
            return 0

        # First argument to CFUNCTYPE is the return type:
        callback = _portaudio.PaStreamCallback(_callback)

        err = _portaudio.Pa_OpenStream(byref(self.stream),
                                        None,#byref(self.input_parameters),
                                        byref(self.output_parameters),
                                        self.sample_rate,
                                        self.frames_per_buffer,
                                        self.flags,
                                        byref(callback),
                                        byref(self.data))
        try:
            raise get_exception(err)
        except NoError:
            print 'stream opened'

    def callback(self):
        print 'in callback'

    def read(self, size):
        pass

    def write(self, bytes):
        buff_constructor = c_float * self.frames_per_buffer
        buff = buff_constructor(*range(self.frames_per_buffer))
        err = _portaudio.Pa_WriteStream(byref(self.stream), byref(buff), c_ulong(frames_per_buffer))
        try:
            raise get_exception(err)
        except NoError:
            pass

    def close(self):

        err = _portaudio.Pa_CloseStream(byref(self.stream))
        try:
            raise get_exception(err)
        except NoError:
            pass
