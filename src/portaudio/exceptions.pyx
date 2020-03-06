
from .cimport pa

__all__ = [
    # Portaudio exceptions
    'PortAudioException', 'NotInitialized', 'UnanticipatedHostError', 'InvalidChannelCount', 'InvalidSampleRate',
    'InvalidDevice', 'InvalidFlag', 'SampleFormatNotSupported', 'BadIODeviceCombination', 'InsufficientMemory',
    'BufferTooBig', 'BufferTooSmall', 'NullCallback', 'BadStreamPtr', 'TimedOut', 'InternalError', 'DeviceUnavailable',
    'IncompatibleHostApiSpecificStreamInfo', 'StreamIsStopped', 'StreamIsNotStopped', 'InputOverflowed',
    'BufferUnderflowed', 'OutputUnderflowed', 'HostApiNotFound', 'InvalidHostApi', 'CanNotReadFromACallbackStream',
    'CanNotWriteToACallbackStream', 'CanNotReadFromAnOutputOnlyStream', 'CanNotWriteToAnInputOnlyStream',
    'IncompatibleStreamHostApi', 'BadBufferPtr',
    'EXCEPTIONS', 'check_error',

    # Non-portaudio exceptions
    'BufferException', 'BufferUnderflow', 'BufferOverflow', 'CommitMismatch',

]


class PortAudioException(Exception):
    ...


class NotInitialized(PortAudioException):
    ...


class UnanticipatedHostError(PortAudioException):
    ...


class InvalidChannelCount(PortAudioException):
    ...


class InvalidSampleRate(PortAudioException):
    ...


class InvalidDevice(PortAudioException):
    ...


class InvalidFlag(PortAudioException):
    ...


class SampleFormatNotSupported(PortAudioException):
    ...


class BadIODeviceCombination(PortAudioException):
    ...


class InsufficientMemory(PortAudioException):
    ...


class BufferTooBig(PortAudioException):
    ...


class BufferTooSmall(PortAudioException):
    ...


class NullCallback(PortAudioException):
    ...


class BadStreamPtr(PortAudioException):
    ...


class TimedOut(PortAudioException):
    ...


class InternalError(PortAudioException):
    ...


class DeviceUnavailable(PortAudioException):
    ...


class IncompatibleHostApiSpecificStreamInfo(PortAudioException):
    ...


class StreamIsStopped(PortAudioException):
    ...


class StreamIsNotStopped(PortAudioException):
    ...


class InputOverflowed(PortAudioException):
    ...


class BufferUnderflowed(PortAudioException):
    ...


class OutputUnderflowed(BufferUnderflowed):
    ...


class HostApiNotFound(BufferUnderflowed):
    ...


class InvalidHostApi(PortAudioException):
    ...


class CanNotReadFromACallbackStream(PortAudioException):
    ...


class CanNotWriteToACallbackStream(PortAudioException):
    ...


class CanNotReadFromAnOutputOnlyStream(PortAudioException):
    ...


class CanNotWriteToAnInputOnlyStream(PortAudioException):
    ...


class IncompatibleStreamHostApi(PortAudioException):
    ...


class BadBufferPtr(PortAudioException):
    ...


# Non-portaudio exceptions
class BufferException(Exception):
    ...


class BufferOverflow(BufferException):
    ...


class BufferUnderflow(BufferException):
    ...


class CommitMismatch(BufferException):
    ...


EXCEPTIONS = {
    pa.paNotInitialized: NotInitialized,
    pa.paUnanticipatedHostError: UnanticipatedHostError,
    pa.paInvalidChannelCount: InvalidChannelCount,
    pa.paInvalidSampleRate: InvalidSampleRate,
    pa.paInvalidDevice: InvalidDevice,
    pa.paInvalidFlag: InvalidFlag,
    pa.paSampleFormatNotSupported: SampleFormatNotSupported,
    pa.paBadIODeviceCombination: BadIODeviceCombination,
    pa.paInsufficientMemory: InsufficientMemory,
    pa.paBufferTooBig: BufferTooBig,
    pa.paBufferTooSmall: BufferTooSmall,
    pa.paNullCallback: NullCallback,
    pa.paBadStreamPtr: BadStreamPtr,
    pa.paTimedOut: TimedOut,
    pa.paInternalError: InternalError,
    pa.paDeviceUnavailable: DeviceUnavailable,
    pa.paIncompatibleHostApiSpecificStreamInfo: IncompatibleHostApiSpecificStreamInfo,
    pa.paStreamIsStopped: StreamIsStopped,
    pa.paStreamIsNotStopped: StreamIsNotStopped,
    pa.paInputOverflowed: InputOverflowed,
    pa.paOutputUnderflowed: OutputUnderflowed,
    pa.paHostApiNotFound: HostApiNotFound,
    pa.paInvalidHostApi: InvalidHostApi,
    pa.paCanNotReadFromACallbackStream: CanNotReadFromACallbackStream,
    pa.paCanNotWriteToACallbackStream: CanNotWriteToACallbackStream,
    pa.paCanNotReadFromAnOutputOnlyStream: CanNotReadFromAnOutputOnlyStream,
    pa.paCanNotWriteToAnInputOnlyStream: CanNotWriteToAnInputOnlyStream,
    pa.paIncompatibleStreamHostApi: IncompatibleStreamHostApi,
    pa.paBadBufferPtr: BadBufferPtr,
}


def check_error(err: int) -> int:
    if err != pa.paNoError:
        exc_class = EXCEPTIONS.get(err, PortAudioException)
        raise exc_class('%s (PaErrorCode %s)' % (pa.Pa_GetErrorText(err).decode('utf8'), err))
    return err
