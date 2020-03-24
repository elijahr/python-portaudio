# distutils: language = c++

from ringbuf.boost cimport spsc_queue


# A container for buffer communication between Python code and PortAudio stream callbacks
ctypedef struct duplex_buffer_t:
    spsc_queue[char]* queue[2]
    unsigned short itemsize[2]
    unsigned short channels[2]
    bint interleaved
    bint stopping

    unsigned long long input_pa_overflows
    unsigned long long input_pa_underflows
    unsigned long long input_ringbuf_overflows
    unsigned long long output_pa_overflows
    unsigned long long output_pa_underflows
    unsigned long long output_ringbuf_underflows
