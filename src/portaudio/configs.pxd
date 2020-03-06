
from . cimport pa


cdef class Device:
    cdef:
        readonly int index
        pa.PaDeviceInfo* info


cdef class AbstractConfig:
    cdef:
        pa.PaStreamParameters* params
        object _device
        readonly str struct_format


cdef class Input(AbstractConfig):
    pass


cdef class Output(AbstractConfig):
    pass