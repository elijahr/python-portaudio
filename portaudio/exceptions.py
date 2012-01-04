
import _portaudio as _pa

class PortAudioError(BaseException):

    def __repr__(self):
        return '<%s()>' % (self.__class__.__name__)

    def __unicode__(self):
        return unicode(self.error_code)

    def __str__(self):
        return str(self.error_code)

class NoError(PortAudioError):
    error_code = _pa.paNoError

class NotInitialized(PortAudioError):
    error_code = _pa.paNotInitialized

class UnanticipatedHostError(PortAudioError):
    error_code = _pa.paUnanticipatedHostError

class InvalidChannelCount(PortAudioError):
    error_code = _pa.paInvalidChannelCount

class InvalidSampleRate(PortAudioError):
    error_code = _pa.paInvalidSampleRate

class InvalidDevice(PortAudioError):
    error_code = _pa.paInvalidDevice

class InvalidFlag(PortAudioError):
    error_code = _pa.paInvalidFlag

class SampleFormatNotSupported(PortAudioError):
    error_code = _pa.paSampleFormatNotSupported

class BadIODeviceCombination(PortAudioError):
    error_code = _pa.paBadIODeviceCombination

class InsufficientMemory(PortAudioError):
    error_code = _pa.paInsufficientMemory

class BufferTooBig(PortAudioError):
    error_code = _pa.paBufferTooBig

class BufferTooSmall(PortAudioError):
    error_code = _pa.paBufferTooSmall

class NullCallback(PortAudioError):
    error_code = _pa.paNullCallback

class BadStreamPointer(PortAudioError):
    error_code = _pa.paBadStreamPtr

class TimedOut(PortAudioError):
    error_code = _pa.paTimedOut

class InternalError(PortAudioError):
    error_code = _pa.paInternalError

class DeviceUnavailable(PortAudioError):
    error_code = _pa.paDeviceUnavailable

class IncompatibleHostApiSpecificStreamInfo(PortAudioError):
    error_code = _pa.paIncompatibleHostApiSpecificStreamInfo

class StreamIsStopped(PortAudioError):
    error_code = _pa.paStreamIsStopped

class StreamIsNotStopped(PortAudioError):
    error_code = _pa.paStreamIsNotStopped

class InputOverflowed(PortAudioError):
    error_code = _pa.paInputOverflowed

class OutputUnderflowed(PortAudioError):
    error_code = _pa.paOutputUnderflowed

class HostApiNotFound(PortAudioError):
    error_code = _pa.paHostApiNotFound

class InvalidHostApi(PortAudioError):
    error_code = _pa.paInvalidHostApi

class CanNotReadFromACallbackStream(PortAudioError):
    error_code = _pa.paCanNotReadFromACallbackStream

class CanNotWriteToACallbackStream(PortAudioError):
    error_code = _pa.paCanNotWriteToACallbackStream

class CanNotReadFromAnOutputOnlyStream(PortAudioError):
    error_code = _pa.paCanNotReadFromAnOutputOnlyStream

class CanNotWriteToAnInputOnlyStream(PortAudioError):
    error_code = _pa.paCanNotWriteToAnInputOnlyStream

class IncompatibleStreamHostApi(PortAudioError):
    error_code = _pa.paIncompatibleStreamHostApi

class BadBufferPointer(PortAudioError):
    error_code = _pa.paBadBufferPtr

exceptions = (NoError,
              NotInitialized,
              UnanticipatedHostError,
              InvalidChannelCount,
              InvalidSampleRate,
              InvalidDevice,
              InvalidFlag,
              SampleFormatNotSupported,
              BadIODeviceCombination,
              InsufficientMemory,
              BufferTooBig,
              BufferTooSmall,
              NullCallback,
              BadStreamPointer,
              TimedOut,
              InternalError,
              DeviceUnavailable,
              IncompatibleHostApiSpecificStreamInfo,
              StreamIsStopped,
              StreamIsNotStopped,
              InputOverflowed,
              OutputUnderflowed,
              HostApiNotFound,
              InvalidHostApi,
              CanNotReadFromACallbackStream,
              CanNotWriteToACallbackStream,
              CanNotReadFromAnOutputOnlyStream,
              CanNotWriteToAnInputOnlyStream,
              IncompatibleStreamHostApi,
              BadBufferPointer)

class UnknownPortAudioError(PortAudioError):
    def __init__(self):
        self.error_code = None
        super(PortAudioError, self).__init__()

def get_exception(code):
    """
    Raise an exception corresponding to a PortAudio error code
    """
    for exception_class in exceptions:
        if exception_class.error_code == code:
            return exception_class()
    exception = UnknownPortAudioError()
    exception.error_code = code
    return exception
