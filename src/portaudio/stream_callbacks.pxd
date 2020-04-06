
from . cimport pa


cdef pa.PaError callback_input(
    const void *in_buffer,
    void *out_buffer,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_queue
) nogil

cdef pa.PaError callback_output(
    const void *in_buffer,
    void *out_buffer,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_queue
) nogil

cdef pa.PaError callback_duplex(
    const void *in_buffer,
    void *out_buffer,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_queue
) nogil

cdef pa.PaError callback_null(
    const void *in_data,
    void *out_data,
    unsigned long frames_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil