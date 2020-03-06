
from . cimport pa


cdef pa.PaError callback_input(
    const void *in_buffer,
    void *out_buffer,
    unsigned long samples_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_queue
) nogil

cdef pa.PaError callback_output(
    const void *in_buffer,
    void *out_buffer,
    unsigned long samples_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_queue
) nogil

cdef pa.PaError callback_duplex(
    const void *in_buffer,
    void *out_buffer,
    unsigned long samples_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_queue
) nogil