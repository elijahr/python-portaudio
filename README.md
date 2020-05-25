python-portaudio
================

asyncio-friendly Python bindings for the [PortAudio](http://www.portaudio.com/) audio I/O library.

Alpha-quality at the moment.


`shape[0]` is the number of rows. For interleaved data, this would be `size / channels`. For non interleaved data,
this is `channels`.

`shape[1]` is the number of columns. For interleaved data, this is `channels`. For non interleaved data, this is
`size / channels`.

`stride[0]` is the distance between the first elements of adjacent channels.
`stride[1]` is the distance, in bytes, between two samples in the same channel.

```
                                                    strides[0]
                                                   /¯\
If (stereo) data is interleaved, it's of the form [L, R, L, R, L, R]
                                                   \____/
                                                    strides[1]

                                                        strides[1]
                                                       /¯¯¯¯¯¯¯\
If (stereo) data is not interleaved, it's of the form [L, L, L, R, R, R]
                                                       \_/
                                                        strides[0]
```
