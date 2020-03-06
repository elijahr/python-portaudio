
from .pthread cimport pthread_cond_t, pthread_mutex_t

cdef extern from "bipbuffer.h" nogil:

    cdef enum ERROR:
        NO_ERROR = 0
        ERR_UNDERFLOW = -100
        ERR_COMMIT_MISMATCH

    cdef struct region:
        long int start
        long int end

    cdef struct bipbuffer:
        char* data
        long int size
        region a
        region b
        short read_from
        short write_to
        long int allocated
        pthread_cond_t cond
        pthread_mutex_t mutex

    bipbuffer* bb_create(long int size)

    void bb_destroy(bipbuffer* bip)

    void bb_clear(bipbuffer* bip)

    void* bb_alloc(bipbuffer* bip, long int size, bint block)

    int bb_commit(bipbuffer* bip, long int size)

    long int bb_read(bipbuffer* bip, void* dst, long int size, bint block)

    long int bb_look(bipbuffer* bip, void* dst, long int size)


cdef class AudioBuffer:
    # The underlying BipBuffer struct
    cdef:
        bipbuffer* bip

        # The data's format character, specifying the type and bytesize of samples
        # see https://docs.python.org/3/library/struct.html#format-characters
        readonly str struct_format

        # The number of channels in the buffer. Usually 1 (mono) or 2 (stereo).
        readonly unsigned short channels

        # Whether the multi-channel data is interleaved or not
        # (i.e. interleaved is [L, R, L R], non-interleaved is [L, L, R, R])
        readonly bint interleaved
        #
        # # The number of samples in the buffer, total, across all channels
        #     readonly unsigned long int size

        # The number of bytes per sample, as determined by format
        readonly size_t itemsize

        # Shape cache
        dict _shapes

        tuple _get_shape(AudioBuffer self, unsigned long int samples)


# A container for buffer communication between the producer/consumer threads and the PortAudio stream callbacks
ctypedef struct duplex_buffer_t:
    bipbuffer* bip[2]
    unsigned long int itemsize[2]
