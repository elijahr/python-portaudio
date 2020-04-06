import logging
from time import sleep
from typing import Union, Tuple

# This unused cimport is necessary to initialize threads such that non-Python threads
# can acquire the GIL
cimport cython.parallel

from libc.string cimport memset

from cpython.ref cimport Py_DECREF, Py_INCREF
from ringbuf.ringbuf cimport RingBuffer
from . import exceptions, stream_helpers
from . cimport configs, stream_callbacks
from .pa import ACTIVE_STREAMS


logger = logging.getLogger('portaudio')


__all__ = ['Stream']


ConfigType = Union[
    configs.Input,
    configs.Output,
    Tuple[configs.Input, configs.Output],
]


DEFAULT_RINGBUFFER_CAPACITY = 44100


cdef class Stream:
    def __cinit__(
            self,
            *,
            config: ConfigType,
            sample_rate: Union[float, int, None] = None,
            frames_per_buffer: int = pa.paFramesPerBufferUnspecified,
            ringbuffer_capacity=DEFAULT_RINGBUFFER_CAPACITY,
            clip: bool = True,
            dither: bool = False,
            never_drop_input: bool = False,
            prime_output_buffers: bool = False,
            null: bool = False,
            **kwargs  # kwargs provided to allow user subclassing
    ):
        self.stream = NULL
        self.flags = pa.paNoFlag

        if isinstance(config, configs.Input):
            self.config = (config, None)
        elif isinstance(config, configs.Output):
            self.config = (None, config)
        else:
            self.config = tuple(sorted(config, key=lambda c: 0 if isinstance(c, configs.Input) else 1))

        if not any(self.config):
            raise ValueError('Must provide an input and/or output config')

        cdef:
            RingBuffer buf

        memset(&self.duplex_buffer, 0, sizeof(buffers.duplex_buffer_t))

        buffer = [None, None]
        null_buffer = [None, None]
        for i, conf in enumerate(self.config):
            if not conf:
                continue

            buf = RingBuffer(
                format=conf.struct_format,
                capacity=(
                    frames_per_buffer
                    if frames_per_buffer != pa.paFramesPerBufferUnspecified
                    else DEFAULT_RINGBUFFER_CAPACITY
                ) * conf.channels)

            buffer[i] = buf
            self.duplex_buffer.queue[i] = buf.queue
            self.duplex_buffer.itemsize[i] = buf.itemsize
            self.duplex_buffer.channels[i] = conf.channels

            if null:
                buf = RingBuffer(
                    format=self.config[i].struct_format,
                    capacity=(
                        frames_per_buffer
                        if frames_per_buffer != pa.paFramesPerBufferUnspecified
                        else DEFAULT_RINGBUFFER_CAPACITY
                    ) * conf.channels)
                null_buffer[i] = buf
                self.duplex_buffer.null_queue[i] = buf.queue

        self.buffer = tuple(buffer)
        self.null_buffer = tuple(null_buffer)

        if self.is_duplex:
            self.params[0] = (<configs.Input>self.config[0]).params
            self.params[1] = (<configs.Output>self.config[1]).params

        elif self.is_input_only:
            self.params[0] = (<configs.Input>self.config[0]).params
            self.params[1] = NULL

        else:
            self.params[0] = NULL
            self.params[1] = (<configs.Output>self.config[1]).params

        if null:
            self.callback = stream_callbacks.callback_null
        elif self.is_duplex:
            self.callback = stream_callbacks.callback_duplex
        elif self.is_input_only:
            self.callback = stream_callbacks.callback_input
        else:
            self.callback = stream_callbacks.callback_output

        if sample_rate is None:
            # If no sample rate provided, use the lowest common sample rate for the devices
            sample_rates = []
            for conf in self.config:
                if conf is not None:
                    sample_rates.append(conf.device.default_sample_rate)
            sample_rate = min(sample_rates)

        self.sample_rate = float(sample_rate)
        self.frames_per_buffer = frames_per_buffer

        self.clip = clip
        self.dither = dither
        self.prime_output_buffers = prime_output_buffers
        self.never_drop_input = never_drop_input

    def __init__(
            self,
            *,
            config: ConfigType,
            sample_rate: Union[float, int, None] = None,
            frames_per_buffer: int = pa.paFramesPerBufferUnspecified,
            ringbuffer_capacity=DEFAULT_RINGBUFFER_CAPACITY,
            clip: bool = True,
            dither: bool = False,
            never_drop_input: bool = False,
            prime_output_buffers: bool = False,
            null: bool = False,
            **kwargs
    ):
        ...

    def __repr__(self):
        parts = ['config=%s' % repr(self.config)]
        if self.frames_per_buffer == pa.paFramesPerBufferUnspecified:
            frames_per_buffer = 'FRAMES_PER_BUFFER_UNSPECIFIED'
        else:
            frames_per_buffer = repr(self.frames_per_buffer)
        parts.append('sample_rate=%r, frames_per_buffer=%s' % (self.sample_rate, frames_per_buffer))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))

    # As of this writing, PyPy doesn't work with Cython-compiled coroutines,
    # so they are implemented in pure Python for compatibility.
    write = stream_helpers.stream_write
    read = stream_helpers.stream_read

    def _set_flag(self, enabled: bool, flag: int) -> None:
        if self.running:
            exceptions.check_error(pa.paStreamIsNotStopped)
        self.flags = pa.set_flag(self.flags, enabled, flag)

    @property
    def is_duplex(self) -> bool:
        return all(self.config)

    @property
    def is_input(self) -> bool:
        return self.config[0] is not None

    @property
    def is_output(self) -> bool:
        return self.config[1] is not None

    @property
    def is_input_only(self) -> bool:
        return self.config[0] is not None and self.config[1] is None

    @property
    def is_output_only(self) -> bool:
        return self.config[1] is not None and self.config[0] is None

    @property
    def clip(self) -> bool:
        return not (self.flags & pa.paClipOff)

    @clip.setter
    def clip(self, value: bool) -> None:
        self._set_flag(not value, pa.paClipOff)

    @property
    def dither(self) -> bool:
        return not (self.flags & pa.paDitherOff)

    @dither.setter
    def dither(self, value: bool) -> None:
        self._set_flag(not value, pa.paDitherOff)

    @property
    def never_drop_input(self) -> bool:
        return bool(self.flags & pa.paNeverDropInput)

    @never_drop_input.setter
    def never_drop_input(self, value: bool) -> None:
        if value and not (self.is_duplex and self.frames_per_buffer == pa.paFramesPerBufferUnspecified):
            raise ValueError('This flag can only be set for duplex streams with unspecified frames per buffer.')
        self._set_flag(value, pa.paNeverDropInput)

    @property
    def prime_output_buffers(self) -> bool:
        return bool(self.flags & pa.paPrimeOutputBuffersUsingStreamCallback)

    @prime_output_buffers.setter
    def prime_output_buffers(self, value: bool) -> None:
        self._set_flag(value, pa.paPrimeOutputBuffersUsingStreamCallback)

    def start(self):
        if self.running:
            exceptions.check_error(pa.paStreamIsNotStopped)

        logger.debug('%r: starting' % self)
        Py_INCREF(self)
        ACTIVE_STREAMS.add(self)

        # reset counters
        self.duplex_buffer.input_pa_underflows = 0
        self.duplex_buffer.input_pa_overflows = 0
        self.duplex_buffer.input_ringbuf_overflows = 0
        self.duplex_buffer.output_pa_overflows = 0
        self.duplex_buffer.output_pa_overflows = 0
        self.duplex_buffer.output_ringbuf_underflows = 0

        # reset RingBuffers
        for buffer in self.buffer:
            if buffer:
                buffer.reset()

        try:
            exceptions.check_error(
                pa.Pa_OpenStream(
                    &self.stream,
                    self.params[0],
                    self.params[1],
                    self.sample_rate,
                    self.frames_per_buffer,
                    self.flags,
                    self.callback,
                    <void*>&self.duplex_buffer))
            exceptions.check_error(pa.Pa_StartStream(self.stream))
        except:
            ACTIVE_STREAMS.remove(self)
            raise
        else:
            self.running = True

    def stop(self, abort: bool = False):
        if not self.running:
            exceptions.check_error(pa.paStreamIsStopped)
        if abort:
            exceptions.check_error(pa.Pa_AbortStream(self.stream))
        else:
            # Allow the RingBuffer to drain
            self.duplex_buffer.stopping = True
            while self.active:
                sleep(0.01)
            self.duplex_buffer.stopping = False
            exceptions.check_error(pa.Pa_StopStream(self.stream))
        exceptions.check_error(pa.Pa_CloseStream(self.stream))
        self.running = False
        ACTIVE_STREAMS.remove(self)
        Py_DECREF(self)

    @property
    def stopping(self):
        return self.duplex_buffer.stopping

    @property
    def active(self) -> bool:
        if self.stream is NULL:
            return False
        cdef pa.PaError err = pa.Pa_IsStreamActive(self.stream)
        if err == 0:
            return False
        elif err == 1:
            return True
        else:
            exceptions.check_error(err)

    @property
    def input_capacity(self) -> int:
        return self.buffer[0].capacity if self.buffer[0] else 0

    @property
    def output_capacity(self) -> int:
        return self.buffer[1].capacity if self.buffer[1] else 0

    @property
    def input_read_available(self) -> int:
        return self.buffer[0].read_available

    @property
    def input_write_available(self) -> int:
        return self.buffer[0].write_available

    @property
    def output_read_available(self) -> int:
        return self.buffer[1].read_available

    @property
    def output_write_available(self) -> int:
        return self.buffer[1].write_available

    @property
    def input_pa_underflows(self) -> int:
        return self.duplex_buffer.input_pa_underflows

    @property
    def input_pa_overflows(self) -> int:
        return self.duplex_buffer.input_pa_overflows

    @property
    def input_ringbuf_overflows(self) -> int:
        return self.duplex_buffer.input_ringbuf_overflows

    @property
    def output_pa_underflows(self) -> int:
        return self.duplex_buffer.output_pa_underflows

    @property
    def output_pa_overflows(self) -> int:
        return self.duplex_buffer.output_pa_overflows

    @property
    def output_ringbuf_underflows(self) -> int:
        return self.duplex_buffer.output_ringbuf_underflows
