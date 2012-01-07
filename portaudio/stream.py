
from portaudio.exceptions import get_exception, NoError
from portaudio import flags

from ctypes import *
from portaudio import _portaudio

# these docs are great
# http://portaudio.com/docs/v19-doxydocs/api_overview.html

class PortAudio(object):
    """
    Context manager for using PortAudio
    """
    def __enter__(self):
        try:
            raise get_exception(_portaudio.Pa_Initialize())
        except NoError:
            pass
        return self

    def __exit__(self, type, value, traceback):
        err = _portaudio.Pa_Terminate()
        try:
            raise get_exception(err)
        except NoError:
            pass

class Stream(object):

    def __init__(self):
        self.sample_rate = 44100
        self.frames_per_buffer = 200
        self.flags = _portaudio.paClipOff
        self.stream = POINTER(c_void_p)()

    def __enter__(self):
        self.open()
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.close()

    def open(self):
        output_parameters = _portaudio.PaStreamParameters()
        output_parameters.device = _portaudio.Pa_GetDefaultOutputDevice()
        assert output_parameters.device != _portaudio.paNoDevice
        output_parameters.channelCount = 2
        output_parameters.sampleFormat = _portaudio.paFloat32
        device_info = _portaudio.Pa_GetDeviceInfo( output_parameters.device )
        output_parameters.suggestedLatency = device_info.contents.defaultLowOutputLatency;
        output_parameters.hostApiSpecificStreamInfo = None

        err = _portaudio.Pa_OpenStream(byref(self.stream),
                                       None,
                                       byref(output_parameters),
                                       self.sample_rate,
                                       c_ulong(self.frames_per_buffer),
                                       self.flags,
                                       None,
                                       None)

        try:
            raise get_exception(err)
        except NoError:
            print('stream opened')


    def read(self, size):
        pass

    def stop(self):
        err = _portaudio.Pa_StopStream(self.stream)
        try:
            raise get_exception(err)
        except NoError:
            print('stream stopped')

    def start(self):
        err = _portaudio.Pa_StartStream(self.stream)
        try:
            raise get_exception(err)
        except NoError:
            print('stream started')

    def write(self, bytes):
        print(_portaudio.Pa_GetStreamWriteAvailable(self.stream))
        buff_constructor = c_float * self.frames_per_buffer
        buff = buff_constructor(*range(self.frames_per_buffer))
        err = _portaudio.Pa_WriteStream(self.stream, byref(buff), c_ulong(self.frames_per_buffer))
        try:
            raise get_exception(err)
        except NoError:
            pass

    def close(self):
        err = _portaudio.Pa_CloseStream(self.stream)
        try:
            raise get_exception(err)
        except NoError:
            print('stream stopped')
