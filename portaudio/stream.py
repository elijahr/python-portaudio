
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

    def build_input_parameters(self, device=None,
                                sample_format=_portaudio.paFloat32,
                                suggested_latency=None):
        input_parameters = _portaudio.PaStreamParameters()

        # set the device
        if device is None:
            device = _portaudio.Pa_GetDefaultInputDevice()
        input_parameters.device = device
        assert input_parameters.device != _portaudio.paNoDevice

        input_parameters.channelCount = self.channel_count
        input_parameters.sampleFormat = sample_format

        # set the suggested output latency
        if suggested_latency is None:
            device_info = _portaudio.Pa_GetDeviceInfo( input_parameters.device )
            suggested_latency = device_info.contents.defaultLowOutputLatency
        input_parameters.suggestedLatency = suggested_latency

        input_parameters.hostApiSpecificStreamInfo = None
        return input_parameters

    def open(self, mode='rw', input_parameters=None, output_parameters=None):
        if 'w' in mode:
            output_parameters_ref = byref(output_parameters or self.build_output_parameters())
        else:
            output_parameters_ref = None
        if 'r' in mode:
            input_parameters_ref = byref(input_parameters or self.build_input_parameters())
        else:
            input_parameters_ref = None

        err = _portaudio.Pa_OpenStream(byref(self.stream),
                                       input_parameters_ref,
                                       output_parameters_ref,
                                       self.sample_rate,
                                       c_ulong(self.frames_per_buffer),
                                       self.flags,
                                       None,
                                       None)

        try:
            raise get_exception(err)
        except NoError:
            pass

    def close(self):
        err = _portaudio.Pa_CloseStream(self.stream)
        try:
            raise get_exception(err)
        except NoError:
            pass

    def start(self):
        err = _portaudio.Pa_StartStream(self.stream)
        try:
            raise get_exception(err)
        except NoError:
            pass

    def stop(self):
        err = _portaudio.Pa_StopStream(self.stream)
        try:
            raise get_exception(err)
        except NoError:
            pass

    def read(self, size=None):
        if size is None:
            size = self.frames_per_buffer

        value = _portaudio.Pa_GetStreamReadAvailable(self.stream)
        if value < 0:
            # if value is negative, its a PaError code
            try:
                raise get_exception(value)
            except NoError:
                pass

        buff = c_void_p()
        err = _portaudio.Pa_ReadStream(self.stream, byref(buff), c_ulong(size))
        try:
            raise get_exception(err)
        except NoError:
            pass

        return buff

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

        err = _portaudio.Pa_WriteStream(self.stream, byref(buff), c_ulong(frames_per_buffer))
        try:
            raise get_exception(err)
        except NoError:
            pass
