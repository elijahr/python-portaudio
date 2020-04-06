


from . cimport buffers, pa


cdef class Stream:
    cdef:
         readonly bint running
         readonly double sample_rate
         readonly int frames_per_buffer
         readonly unsigned long flags

         readonly tuple config
         readonly tuple buffer
         buffers.duplex_buffer_t duplex_buffer

         readonly tuple null_buffer

         pa.PaStream * stream
         pa.PaStreamCallback* callback
         pa.PaStreamParameters* params[2]

