import struct
import threading
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


__all__ = ['Stream']


ConfigType = Union[
    configs.Input,
    configs.Output,
    Tuple[configs.Input, configs.Output],
]


DEFAULT_RINGBUF_CAPACITY = 44100 * 10


cdef class Stream:
    def __cinit__(
        self,
        *,
        config: ConfigType,
        sample_rate: Union[float, int, None] = None,
        samples_per_buffer: int = pa.paFramesPerBufferUnspecified,
        flags: int = pa.paClipOff,
        ringbuf_capacity=DEFAULT_RINGBUF_CAPACITY,
        **kwargs
    ):
        self.stream = NULL
        self.flags = flags

        if isinstance(config, configs.Input):
            self.config = (config, None)
            # self.iterator = stream_helpers.InputStreamIterator(self)
        elif isinstance(config, configs.Output):
            self.config = (None, config)
            # self.iterator = stream_helpers.OutputStreamIterator(self)
        else:
            self.config = tuple(sorted(config, key=lambda c: 0 if isinstance(c, configs.Input) else 1))
            # self.iterator = stream_helpers.DuplexStreamIterator(self)

        cdef:
            RingBuffer buf

        memset(&self.duplex_buffer, 0, sizeof(buffers.duplex_buffer_t))

        buffer = [None, None]
        for i, config in enumerate(self.config):
            if not config:
                continue

            buf = RingBuffer(
                format=config.struct_format,
                capacity=(
                    samples_per_buffer
                    if samples_per_buffer != pa.paFramesPerBufferUnspecified
                    else DEFAULT_RINGBUF_CAPACITY
                ) * config.channels)

            buffer[i] = buf
            self.duplex_buffer.queue[i] = buf.queue
            self.duplex_buffer.itemsize[i] = struct.calcsize(config.struct_format)
            self.duplex_buffer.channels[i] = config.channels

        self.buffer = tuple(buffer)

        if sample_rate is None:
            # If no sample rate provided, use the lowest common sample rate for the devices
            sample_rates = []
            for config in self.config:
                if config is not None:
                    sample_rates.append(config.device.default_sample_rate)
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
        flags: int = pa.paClipOff,
        ringbuf_capacity=DEFAULT_RINGBUF_CAPACITY,
        **kwargs
    ):
        ...

    def __repr__(Stream self):
        parts = []
        if self.config[0]:
            parts.append('in_config=%r' % self.config[0])
        if self.config[1]:
            parts.append('out_config=%r' % self.config[1])
        if self.samples_per_buffer == pa.paFramesPerBufferUnspecified:
            samples_per_buffer = 'FRAMES_PER_BUFFER_UNSPECIFIED'
        else:
            samples_per_buffer = repr(self.samples_per_buffer)
        parts.append('sample_rate=%r, samples_per_buffer=%s' % (self.sample_rate, samples_per_buffer))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))

    write = stream_helpers.stream_write
    read = stream_helpers.stream_read

    @property
    def interleaved(Stream self):
        return not (self.flags & pa.paNonInterleaved)

    def start(Stream self, flags: pa.PaStreamFlags = pa.paClipOff):
        cdef:
            pa.PaStreamParameters* in_params = NULL
            pa.PaStreamParameters* out_params = NULL
            pa.PaStreamCallback* stream_callback
            const char* err_text

        with self.lock:
            if self.running:
                err_text = pa.Pa_GetErrorText(pa.paStreamIsNotStopped)
                raise exceptions.StreamIsNotStopped(err_text)

            # Steal a ref
            Py_INCREF(self)

            if self.config[0] and self.config[1]:
                in_params = (<configs.Input>self.config[0]).params
                out_params = (<configs.Output>self.config[1]).params
                stream_callback = <pa.PaStreamCallback*>stream_callbacks.callback_duplex

            elif self.config[0]:
                in_params = (<configs.Input>self.config[0]).params
                stream_callback = <pa.PaStreamCallback*>stream_callbacks.callback_input

            elif self.config[1]:
                out_params = (<configs.Output>self.config[1]).params
                stream_callback = <pa.PaStreamCallback*>stream_callbacks.callback_output

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
                exceptions.check_error(pa.paStreamIsStopped)
            if abort:
                exceptions.check_error(pa.Pa_AbortStream(self.stream))
            else:
                if self.buffer[1]:
                    # Allow the RingBuffer to drain
                    self.duplex_buffer.stopping = True
                    while self.active:
                        sleep(0.01)
                    self.duplex_buffer.stopping = False
                exceptions.check_error(pa.Pa_StopStream(self.stream))
            exceptions.check_error(pa.Pa_CloseStream(self.stream))
            self.running = False
            Py_DECREF(self)

    @property
    def stopping(self):
        return self.duplex_buffer.stopping

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
