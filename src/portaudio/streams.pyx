import threading
from typing import Union, Tuple

# This unused cimport is necessary to initialize threads such that non-Python threads
# can acquire the GIL
cimport cython.parallel

from cpython.ref cimport Py_DECREF, Py_INCREF

from . import exceptions
from . cimport buffers, configs, stream_callbacks

from .stream_helpers import AbstractStreamIterator, DuplexStreamIterator, InputStreamIterator, OutputStreamIterator


__all__ = ['Stream']


ConfigType = Union[
    configs.Input,
    configs.Output,
    Tuple[configs.Input, configs.Output],
]


DEFAULT_BIP_SIZE = 44100


cdef class Stream:
    def __cinit__(
        self,
        *,
        config: ConfigType,
        sample_rate: Union[float, int, None] = None,
        samples_per_buffer: int = pa.paFramesPerBufferUnspecified,
        bip_size: int = DEFAULT_BIP_SIZE,
        flags: int = pa.paClipOff,
        **kwargs
    ):
        self.stream = NULL
        self.bip_size = bip_size

        if isinstance(config, configs.Input):
            self.config = (config, None)
            self.iterator = InputStreamIterator(self)
        elif isinstance(config, configs.Output):
            self.config = (None, config)
            self.iterator = OutputStreamIterator(self)
        else:
            self.config = tuple(sorted(config, key=lambda c: 0 if isinstance(c, configs.Input) else 1))
            self.iterator = DuplexStreamIterator(self)

        buffer = [None, None]
        for i, config in enumerate(self.config):
            if config:
                buffer[i] = buffers.AudioBuffer(
                    struct_format=config.struct_format,
                    size=self.bip_size,
                    channels=config.channels,
                    interleaved=self.interleaved)
                self.duplex_buffer.bip[i] = (<buffers.AudioBuffer>buffer[i]).bip
                self.duplex_buffer.itemsize[i] = buffer[i].itemsize
        self.buffer = tuple(buffer)

        if sample_rate is None:
            # If no sample rate provided, use the lowest common sample rate for the devices
            sample_rates = []
            for c in self.config:
                if c is not None:
                    sample_rates.append(c.device.default_sample_rate)
            sample_rate = min(sample_rates)

        self.sample_rate = float(sample_rate)
        self.samples_per_buffer = samples_per_buffer
        self.lock = threading.RLock()

    def __init__(
        self,
        *,
        config: ConfigType,
        sample_rate: Union[float, int, None] = None,
        samples_per_buffer: int = pa.paFramesPerBufferUnspecified,
        bip_size: int = DEFAULT_BIP_SIZE,
        flags: int = pa.paClipOff,
        **kwargs
    ):
        ...

    def __repr__(Stream self):
        parts = []
        if self.config[0]:
            parts.append('in_config=%r' % self.config[0])
        if self.config[1]:
            parts.append('out_config=%r' % self.config[1])
        parts.append('sample_rate=%r, samples_per_buffer=%r' % (self.sample_rate, self.samples_per_buffer))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))

    @property
    def interleaved(Stream self):
        return not (self.flags & pa.paNonInterleaved)

    def start(Stream self, flags: pa.PaStreamFlags = pa.paClipOff):
        cdef:
            pa.PaStreamParameters* in_params = NULL
            pa.PaStreamParameters* out_params = NULL
            pa.PaStreamCallback* stream_callback

        with self.lock:
            if self.running:
                raise exceptions.StreamIsNotStopped(pa.Pa_GetErrorText(pa.paStreamIsNotStopped))

            # Steal a ref
            Py_INCREF(self)

            print("HEY 1", self.config)
            print(0)
            print(1)
            print("HEY 2", self.config[0], self.config[1])
            if self.config[0] and self.config[1]:
                in_params = (<configs.Input>self.config[0]).params
                out_params = (<configs.Output>self.config[1]).params
                stream_callback = <pa.PaStreamCallback*>stream_callbacks.callback_duplex

            elif self.config[0]:
                in_params = (<configs.Input>self.config[0]).params
                stream_callback = <pa.PaStreamCallback*>stream_callbacks.callback_input

            elif self.config[1]:
                print("HEY 3")
                out_params = (<configs.Output>self.config[1]).params
                stream_callback = <pa.PaStreamCallback*>stream_callbacks.callback_output
                print("HEY 4")

            print("out_params.channelCount", out_params.channelCount)
            try:
                exceptions.check_error(
                    pa.Pa_OpenStream(
                        &self.stream,
                        in_params,
                        out_params,
                        self.sample_rate,
                        self.samples_per_buffer,
                        self.flags,
                        stream_callback,
                        <void*>&self.duplex_buffer))
                exceptions.check_error(pa.Pa_StartStream(self.stream))
            except:
                Py_DECREF(self)
                raise
            else:
                self.running = True

    def stop(Stream self, abort: bool = False):
        with self.lock:
            if not self.running:
                raise exceptions.check_error(pa.paStreamIsStopped)
            if abort:
                exceptions.check_error(pa.Pa_AbortStream(self.stream))
            else:
                exceptions.check_error(pa.Pa_StopStream(self.stream))
            exceptions.check_error(pa.Pa_CloseStream(self.stream))
            self.running = False
            Py_DECREF(self)

    @property
    def active(Stream self) -> bool:
        if self.stream is NULL:
            return False
        cdef pa.PaError err = pa.Pa_IsStreamActive(self.stream)
        if err == 0:
            return False
        elif err == 1:
            return True
        else:
            exceptions.check_error(err)

    def __aiter__(Stream self) -> AbstractStreamIterator:
        try:
            self.start()
        except exceptions.StreamIsNotStopped:
            pass
        return self.iterator



