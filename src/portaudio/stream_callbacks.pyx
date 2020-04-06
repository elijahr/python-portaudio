
from libc.stdlib cimport malloc, free
from libc.string cimport memset

from .buffers cimport duplex_buffer_t

from . cimport pa


cdef pa.PaError callback_input(
    const void *in_data,
    void *out_data,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    const pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    cdef:
        duplex_buffer_t* duplex_buffer = <duplex_buffer_t*>_duplex_buffer
        size_t total = frames_per_buffer * duplex_buffer.itemsize[0] * duplex_buffer.channels[0]
        size_t remaining
        char* input = <char*>in_data
        unsigned short i = 0

    if duplex_buffer.stopping:
        return pa.paComplete

    if status_flags & pa.paInputUnderflow:
        duplex_buffer.input_pa_underflows += 1

    if status_flags & pa.paInputOverflow:
        duplex_buffer.input_pa_overflows += 1

    remaining = duplex_buffer.queue[0].push(input, total)
    if remaining:
        duplex_buffer.input_ringbuf_overflows += 1

    return pa.paContinue


cdef pa.PaError callback_output(
    const void *in_data,
    void *out_data,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    const pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    cdef:
        duplex_buffer_t* duplex_buffer = <duplex_buffer_t*>_duplex_buffer
        size_t size = frames_per_buffer * duplex_buffer.itemsize[1] * duplex_buffer.channels[1]
        size_t popped
        char* out = <char*>out_data

    if status_flags & pa.paOutputUnderflow:
        duplex_buffer.output_pa_underflows += 1

    if status_flags & pa.paOutputOverflow:
        duplex_buffer.output_pa_overflows += 1

    popped = duplex_buffer.queue[1].pop(out, size)

    if popped < size:
        # Underflow, write silence
        memset(<void*>&out[popped], 0, size - popped)
        duplex_buffer.output_ringbuf_underflows += 1

    if duplex_buffer.stopping and duplex_buffer.queue[1].read_available() == 0:
        return pa.paComplete

    return pa.paContinue


cdef pa.PaError callback_duplex(
    const void *in_data,
    void *out_data,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    callback_input(in_data, NULL, frames_per_buffer, time_info, status_flags, _duplex_buffer)
    return callback_output(NULL, out_data, frames_per_buffer, time_info, status_flags, _duplex_buffer)


cdef pa.PaError callback_null(
    const void *in_data,
    void *out_data,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    cdef:
        duplex_buffer_t* duplex_buffer = <duplex_buffer_t*>_duplex_buffer
        pa.PaError retval = pa.paAbort
        size_t size
        size_t remaining
        size_t popped
        char* tmp

    if duplex_buffer.queue[0] is not NULL:
        size = frames_per_buffer * duplex_buffer.itemsize[0] * duplex_buffer.channels[0]
        tmp = <char*>malloc(size)
        popped = 0
        while popped < size:
            popped += duplex_buffer.null_queue[0].pop(&tmp[popped], size)
        retval = callback_input(<void*>tmp, NULL, frames_per_buffer, time_info, status_flags, _duplex_buffer)

    if duplex_buffer.queue[1] is not NULL:
        size = frames_per_buffer * duplex_buffer.itemsize[1] * duplex_buffer.channels[1]
        tmp = <char*>malloc(size)
        retval = callback_output(NULL, <void*>tmp, frames_per_buffer, time_info, status_flags, _duplex_buffer)
        remaining = size
        while remaining > 0:
            remaining = duplex_buffer.null_queue[1].push(&tmp[size - remaining], remaining)
        free(tmp)

    if duplex_buffer.queue[1]:
        memset(out_data, 0, size)

    return retval