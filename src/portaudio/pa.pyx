from typing import Union

__all__ = [
    'INITIALIZED',
    'initialize',
    'terminate',

    # ERROR_CODE
    'NO_ERROR', 'NOT_INITIALIZED', 'UNANTICIPATED_HOST_ERROR', 'INVALID_CHANNEL_COUNT', 'INVALID_SAMPLE_RATE',
    'INVALID_DEVICE', 'INVALID_FLAG', 'SAMPLE_FORMAT_NOT_SUPPORTED', 'BAD_IO_DEVICE_COMBINATION',
    'INSUFFICIENT_MEMORY', 'BUFFER_TOO_BIG', 'BUFFER_TOO_SMALL', 'NULL_CALLBACK', 'BAD_STREAM_PTR', 'TIMED_OUT',
    'INTERNAL_ERROR', 'DEVICE_UNAVAILABLE', 'INCOMPATIBLE_HOST_API_SPECIFIC_STREAM_INFO', 'STREAM_IS_STOPPED',
    'STREAM_IS_NOT_STOPPED', 'INPUT_OVERFLOWED', 'OUTPUT_UNDERFLOWED', 'HOST_API_NOT_FOUND', 'INVALID_HOST_API',
    'CAN_NOT_READ_FROM_A_CALLBACK_STREAM', 'CAN_NOT_WRITE_TO_A_CALLBACK_STREAM',
    'CAN_NOT_READ_FROM_AN_OUTPUT_ONLY_STREAM', 'CAN_NOT_WRITE_TO_AN_INPUT_ONLY_STREAM', 'INCOMPATIBLE_STREAM_HOST_API',
    'BAD_BUFFER_PTR',

    # PaStreamCallbackResult
    'CONTINUE', 'COMPLETE', 'ABORT',

    # PaHostApiTypeId
    'IN_DEVELOPMENT', 'DIRECT_SOUND', 'MME', 'ASIO', 'SOUND_MANAGER', 'CORE_AUDIO', 'OSS', 'ALSA',
    'AL', 'BE_OS', 'WDMKS', 'JACK', 'WASAPI', 'AUDIO_SCIENCE_HPI',

    # data formats
    'FLOAT32', 'INT32', 'INT24', 'INT16', 'INT8', 'UINT8',

    # stream flags
    'NO_FLAG', 'CLIP_OFF', 'DITHER_OFF', 'NEVER_DROP_INPUT', 'PRIME_OUTPUT_BUFFERS_USING_STREAM_CALLBACK',
    'PLATFORM_SPECIFIC_FLAGS', 'FRAMES_PER_BUFFER_UNSPECIFIED',

    # callback flags
    'INPUT_UNDERFLOW', 'INPUT_OVERFLOW', 'OUTPUT_UNDERFLOW', 'OUTPUT_OVERFLOW',
    'PRIMING_OUTPUT',

    # other constants
    'NO_DEVICE', 'USE_HOST_API_SPECIFIC_DEVICE_SPECIFICATION', 'FORMAT_IS_SUPPORTED',
]


INITIALIZED = False


def initialize():
    from . import exceptions
    global INITIALIZED
    if not INITIALIZED:
        exceptions.check_error(Pa_Initialize())
        INITIALIZED = True


def terminate(*args, **kwargs):
    from . import exceptions
    global INITIALIZED
    if INITIALIZED:
        exceptions.check_error(Pa_Terminate())
        INITIALIZED = False



NO_DEVICE = paNoDevice
USE_HOST_API_SPECIFIC_DEVICE_SPECIFICATION = paUseHostApiSpecificDeviceSpecification

FORMAT_IS_SUPPORTED = paFormatIsSupported

FLOAT32 = paFloat32
INT32 = paInt32
INT24 = paInt24
INT16 = paInt16
INT8 = paInt8
UINT8 = paUInt8
CUSTOM = paCustomFormat
NON_INTERLEAVED = paNonInterleaved

NO_FLAG = paNoFlag
CLIP_OFF = paClipOff
DITHER_OFF = paDitherOff
NEVER_DROP_INPUT = paNeverDropInput
PRIME_OUTPUT_BUFFERS_USING_STREAM_CALLBACK = paPrimeOutputBuffersUsingStreamCallback
PLATFORM_SPECIFIC_FLAGS = paPlatformSpecificFlags
FRAMES_PER_BUFFER_UNSPECIFIED = paFramesPerBufferUnspecified

INPUT_UNDERFLOW = paInputUnderflow
INPUT_OVERFLOW = paInputOverflow
OUTPUT_UNDERFLOW = paOutputUnderflow
OUTPUT_OVERFLOW = paOutputOverflow
PRIMING_OUTPUT = paPrimingOutput


NO_ERROR = paNoError
NOT_INITIALIZED = paNotInitialized
UNANTICIPATED_HOST_ERROR = paUnanticipatedHostError
INVALID_CHANNEL_COUNT = paInvalidChannelCount
INVALID_SAMPLE_RATE = paInvalidSampleRate
INVALID_DEVICE = paInvalidDevice
INVALID_FLAG = paInvalidFlag
SAMPLE_FORMAT_NOT_SUPPORTED = paSampleFormatNotSupported
BAD_IO_DEVICE_COMBINATION = paBadIODeviceCombination
INSUFFICIENT_MEMORY = paInsufficientMemory
BUFFER_TOO_BIG = paBufferTooBig
BUFFER_TOO_SMALL = paBufferTooSmall
NULL_CALLBACK = paNullCallback
BAD_STREAM_PTR = paBadStreamPtr
TIMED_OUT = paTimedOut
INTERNAL_ERROR = paInternalError
DEVICE_UNAVAILABLE = paDeviceUnavailable
INCOMPATIBLE_HOST_API_SPECIFIC_STREAM_INFO = paIncompatibleHostApiSpecificStreamInfo
STREAM_IS_STOPPED = paStreamIsStopped
STREAM_IS_NOT_STOPPED = paStreamIsNotStopped
INPUT_OVERFLOWED = paInputOverflowed
OUTPUT_UNDERFLOWED = paOutputUnderflowed
HOST_API_NOT_FOUND = paHostApiNotFound
INVALID_HOST_API = paInvalidHostApi
CAN_NOT_READ_FROM_A_CALLBACK_STREAM = paCanNotReadFromACallbackStream
CAN_NOT_WRITE_TO_A_CALLBACK_STREAM = paCanNotWriteToACallbackStream
CAN_NOT_READ_FROM_AN_OUTPUT_ONLY_STREAM = paCanNotReadFromAnOutputOnlyStream
CAN_NOT_WRITE_TO_AN_INPUT_ONLY_STREAM = paCanNotWriteToAnInputOnlyStream
INCOMPATIBLE_STREAM_HOST_API = paIncompatibleStreamHostApi
BAD_BUFFER_PTR = paBadBufferPtr


IN_DEVELOPMENT = paInDevelopment
DIRECT_SOUND = paDirectSound
MME = paMME
ASIO = paASIO
SOUND_MANAGER = paSoundManager
CORE_AUDIO = paCoreAudio
OSS = paOSS
ALSA = paALSA
AL = paAL
BE_OS = paBeOS
WDMKS = paWDMKS
JACK = paJACK
WASAPI = paWASAPI
AUDIO_SCIENCE_HPI = paAudioScienceHPI


CONTINUE = paContinue
COMPLETE = paComplete
ABORT = paAbort


cdef class Nothing:
    pass