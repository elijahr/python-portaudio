

from . cimport buffers, pa


cdef class Stream:
    cdef readonly bint running
    cdef readonly double sample_rate
    cdef readonly int samples_per_buffer
    cdef readonly int bip_size
    cdef readonly int flags
    cdef object lock
    cdef object iterator

    cdef readonly tuple config
    cdef readonly tuple buffer
    cdef buffers.duplex_buffer_t duplex_buffer

    cdef pa.PaStream * stream

