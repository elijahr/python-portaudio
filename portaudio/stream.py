
from portaudio.exceptions import get_exception, NoError
from portaudio import flags

from ctypes import *
from portaudio import _portaudio

# these docs are great
# http://portaudio.com/docs/v19-doxydocs/api_overview.html

class Stream(object):

    def __init__(self, sample_rate=44100, frames_per_buffer=1024,
                 channel_count=2, flags=_portaudio.paClipOff):
        self.sample_rate = sample_rate
        self.frames_per_buffer = frames_per_buffer
        self.channel_count = channel_count
        self.flags = flags
        self.stream = POINTER(c_void_p)()

    def __enter__(self):
        self.open()
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.close()

    def build_output_parameters(self, device=None,
                                sample_format=_portaudio.paFloat32,
                                suggested_latency=None):
        output_parameters = _portaudio.PaStreamParameters()

        # set the device
        if device is None:
            device = _portaudio.Pa_GetDefaultOutputDevice()
        output_parameters.device = device
        assert output_parameters.device != _portaudio.paNoDevice

        output_parameters.channelCount = self.channel_count
        output_parameters.sampleFormat = sample_format

        # set the suggested output latency
        if suggested_latency is None:
            device_info = _portaudio.Pa_GetDeviceInfo( output_parameters.device )
            suggested_latency = device_info.contents.defaultLowOutputLatency
        output_parameters.suggestedLatency = suggested_latency

        output_parameters.hostApiSpecificStreamInfo = None
        return output_parameters

    def open(self, *args, **kwargs):
        output_parameters = self.build_output_parameters(*args, **kwargs)
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

    def write(self, buff, frames_per_buffer):
        if frames_per_buffer is None:
            frames_per_buffer = len(frames_per_buffer)
        value = _portaudio.Pa_GetStreamWriteAvailable(self.stream)
        if value < 0:
            # if value is negative, its a PaError code
            try:
                raise get_exception(value)
            except NoError:
                pass
        else:
            # otherwise its the max number of frames we can write
            print('Max frames to write: %s' % value)

        err = _portaudio.Pa_WriteStream(self.stream, byref(buff), c_ulong(frames_per_buffer))
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
