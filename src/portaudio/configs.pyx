from typing import Union


try:
    import numpy as np
except ImportError:
    np = None


from libc.stdlib cimport malloc, free
from libc.string cimport memset

from . import exceptions, formats
from . cimport pa


__all__ = [
    'Device', 'AbstractConfig', 'Output', 'Input',
]


cdef class Device:
    def __cinit__(self, index: int = -1):
        cdef int device_count = pa.Pa_GetDeviceCount()
        if not device_count:
            raise exceptions.PortAudioException('No available device')

        if index >= device_count:
            raise exceptions.PortAudioException('Invalid device index %s, must be <= %s' % (index, device_count - 1))

        self.index = index

        # Pointer to static object
        self.info = pa.Pa_GetDeviceInfo(index)
        if self.info is NULL:
            raise exceptions.PortAudioException('Invalid device index %s, must be <= %s' % (index, device_count - 1))

    def __init__(self, index: int = -1):
        ...

    def __hash__(self):
        return hash(self.index)

    def __repr__(self):
        return (
            'Device(index=%r, '
            'name=%r, '
            'max_input_channels=%r, '
            'max_output_channels=%r, '
            'default_low_input_latency=%r, '
            'default_low_output_latency=%r, '
            'default_high_input_latency=%r, '
            'default_high_output_latency=%r, '
            'default_sample_rate=%r)'
           ) % (
            self.index,
            self.name,
            self.max_input_channels,
            self.max_output_channels,
            self.default_low_input_latency,
            self.default_low_output_latency,
            self.default_high_input_latency,
            self.default_high_output_latency,
            self.default_sample_rate,
        )

    @property
    def name(self):
        return (<bytes>self.info.name).decode('utf8')

    @property
    def max_input_channels(self):
        return self.info.maxInputChannels

    @property
    def max_output_channels(self):
        return self.info.maxOutputChannels

    @property
    def default_low_input_latency(self):
        return self.info.defaultLowInputLatency

    @property
    def default_low_output_latency(self):
        return self.info.defaultLowOutputLatency

    @property
    def default_high_input_latency(self):
        return self.info.defaultHighInputLatency

    @property
    def default_high_output_latency(self):
        return self.info.defaultHighOutputLatency

    @property
    def default_sample_rate(self):
        return self.info.defaultSampleRate


cdef class AbstractConfig:
    def __cinit__(
        self,
        device: Union[int, Device, None] = pa.paNoDevice,
        channels: Union[int, None] = None,
        format: formats.FormatType = pa.paInt16,
        suggested_latency: Union[float, None] = None
    ):
        self.params = <pa.PaStreamParameters*>malloc(sizeof(pa.PaStreamParameters))
        memset(<void*>self.params, 0, sizeof(pa.PaStreamParameters))

        # Not supported at this time
        self.params.hostApiSpecificStreamInfo = NULL

        print("self.device")
        self.device = device
        print("self.channels")
        self.channels = channels
        print("self.format")
        self.format = format
        print("self.suggested_latency")
        self.suggested_latency = suggested_latency
        print("done")

    def __init__(
        self,
        device: Union[int, Device, None] = pa.paNoDevice,
        channels: Union[int, None] = None,
        format: formats.FormatType = pa.paInt16,
        suggested_latency: Union[float, None] = None
    ):
        ...

    def __dealloc__(self):
        free(self.params)

    def __repr__(AbstractConfig self):
        return '%s(device=%r, channels=%r, format=%s, suggested_latency=%r)' % (
            self.__class__.__name__,
            self.device,
            self.channels,
            formats.FORMAT_NAME[self.format],
            self.suggested_latency,
        )

    @property
    def format(AbstractConfig self) -> int:
        return self.params.sampleFormat

    @format.setter
    def format(AbstractConfig self, value: formats.FormatType):
        # try:
        if np and isinstance(value, np.dtype):
            struct_format = formats.DTYPE_FORMAT[value]
            sample_format = formats.SAMPLE_FORMATS[struct_format]

        elif isinstance(value, int):
            sample_format = value
            struct_format = formats.STRUCT_FORMAT[sample_format]

        elif isinstance(value, str):
            struct_format = value
            sample_format = formats.SAMPLE_FORMATS[struct_format]

        else:
            raise TypeError('Invalid format %r' % value)
        # except KeyError:
        #     raise ValueError('Unsupported format %r' % value)

        self.params.sampleFormat = sample_format
        self.struct_format = struct_format

cdef class Input(AbstractConfig):

    @property
    def device(Input self) -> Device:
        return self._device

    @device.setter
    def device(Input self, value: Union[int, Device]):
        if not isinstance(value, Device):
            if value in (None, pa.paNoDevice):
                value = pa.Pa_GetDefaultInputDevice()
                if value == pa.paNoDevice:
                    raise exceptions.PortAudioException('No available input device')
            value = Device(value)
        self._device = value
        self.params.device = self._device.index

    @property
    def channels(Input self) -> int:
        return self.params.channelCount

    @channels.setter
    def channels(Input self, value: Union[int, None]):
        if value is None:
            value = self._device.max_input_channels

        if value > self._device.max_input_channels:
            raise ValueError('%r: invalid number of input channels' % self)

        self.params.channelCount = value

    @property
    def suggested_latency(Input self) -> float:
        return self.params.suggestedLatency

    @suggested_latency.setter
    def suggested_latency(Input self, value: Union[float, None]):
        if value is None:
            value = self._device.default_low_input_latency
        self.params.suggestedLatency = value


cdef class Output(AbstractConfig):

    @property
    def device(Output self) -> Device:
        return self._device

    @device.setter
    def device(Output self, value: Union[int, Device]):
        if not isinstance(value, Device):
            if value in (None, pa.paNoDevice):
                value = pa.Pa_GetDefaultOutputDevice()
                if value == pa.paNoDevice:
                    raise exceptions.PortAudioException('No available output device')
            value = Device(value)
        self._device = value
        self.params.device = self._device.index

    @property
    def channels(Output self) -> int:
        return self.params.channelCount

    @channels.setter
    def channels(Output self, value: Union[int, None]):
        if value is None:
            value = self._device.max_output_channels

        if value > self._device.max_output_channels:
            raise ValueError('%r: invalid number of output channels' % self)

        self.params.channelCount = value

    @property
    def suggested_latency(Output self) -> float:
        return self.params.suggestedLatency

    @suggested_latency.setter
    def suggested_latency(Output self, value: Union[float, None]):
        if value is None:
            value = self._device.default_low_output_latency
        self.params.suggestedLatency = value