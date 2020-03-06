
from libc.stdio cimport printf
from libc.string cimport memcpy, memset

from .buffers cimport bb_alloc, bb_commit, bb_read, bipbuffer, duplex_buffer_t

from . cimport pa


cdef pa.PaError callback_input(
    const void *in_data,
    void *out_data,
    unsigned long samples_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    cdef:
        duplex_buffer_t* duplex_buffer = <duplex_buffer_t*>_duplex_buffer

        bipbuffer* bip_in = duplex_buffer.bip[0]
        size_t bytesize_in = samples_per_buffer * duplex_buffer.itemsize[0]
        void* tmp

    tmp = <void*>bb_alloc(bip_in, bytesize_in, False)

    if tmp is not NULL:
        memcpy(tmp, in_data, bytesize_in)
        bb_commit(bip_in, bytesize_in)

    return pa.paContinue


cdef pa.PaError callback_output(
    const void *in_data,
    void *out_data,
    unsigned long samples_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    cdef:
        duplex_buffer_t* duplex_buffer = <duplex_buffer_t*>_duplex_buffer

        bipbuffer* bip_out = duplex_buffer.bip[1]
        size_t bytesize_out = samples_per_buffer * duplex_buffer.itemsize[1]
        long int read

    read = bb_read(bip_out, out_data, bytesize_out, False)

    if read <= 0:
        memset(out_data, 0, bytesize_out)

    elif read < bytesize_out:
        # Not enough data in the buffer, write silence to remainder
        memset(out_data + read, 0, bytesize_out - read)

    return pa.paContinue


cdef pa.PaError callback_duplex(
    const void *in_data,
    void *out_data,
    unsigned long samples_per_buffer,
    const pa.PaStreamCallbackTimeInfo* time_info,
    pa.PaStreamCallbackFlags status_flags,
    void *_duplex_buffer
) nogil:
    cdef:
        duplex_buffer_t* duplex_buffer = <duplex_buffer_t*>_duplex_buffer

        bipbuffer* bip_in = duplex_buffer.bip[0]
        size_t bytesize_in = samples_per_buffer * duplex_buffer.itemsize[0]
        void* tmp

        bipbuffer* bip_out = duplex_buffer.bip[1]
        size_t bytesize_out = samples_per_buffer * duplex_buffer.itemsize[1]
        long int read

    tmp = <void*>bb_alloc(bip_in, bytesize_in, False)

    if tmp is not NULL:
        memcpy(tmp, in_data, bytesize_in)
        bb_commit(bip_in, bytesize_in)

    read = bb_read(bip_out, out_data, bytesize_out, False)

    if read <= 0:
        memset(out_data, 0, bytesize_out)

    elif read < bytesize_out:
        # Not enough data in the buffer, write silence to remainder
        memset(out_data + read, 0, bytesize_out - read)

    return pa.paContinue