

cdef extern from "portaudio.h":

    int paNoDevice
    int paUseHostApiSpecificDeviceSpecification

    int paFormatIsSupported
    int paFramesPerBufferUnspecified

    unsigned long paFloat32
    unsigned long paInt32
    unsigned long paInt24
    unsigned long paInt16
    unsigned long paInt8
    unsigned long paUInt8
    unsigned long paCustomFormat
    unsigned long paNonInterleaved

    unsigned long paNoFlag
    unsigned long paClipOff
    unsigned long paDitherOff
    unsigned long paNeverDropInput
    unsigned long paPrimeOutputBuffersUsingStreamCallback
    unsigned long paPlatformSpecificFlags

    unsigned long paInputUnderflow
    unsigned long paInputOverflow
    unsigned long paOutputUnderflow
    unsigned long paOutputOverflow
    unsigned long paPrimingOutput

    ctypedef int PaError
    ctypedef int PaDeviceIndex
    ctypedef int PaHostApiIndex
    ctypedef double PaTime
    ctypedef unsigned long PaSampleFormat
    ctypedef unsigned long PaStreamFlags
    ctypedef unsigned long PaStreamCallbackFlags

    cdef enum PaErrorCode:
        paNoError
        paNotInitialized
        paUnanticipatedHostError
        paInvalidChannelCount
        paInvalidSampleRate
        paInvalidDevice
        paInvalidFlag
        paSampleFormatNotSupported
        paBadIODeviceCombination
        paInsufficientMemory
        paBufferTooBig
        paBufferTooSmall
        paNullCallback
        paBadStreamPtr
        paTimedOut
        paInternalError
        paDeviceUnavailable
        paIncompatibleHostApiSpecificStreamInfo
        paStreamIsStopped
        paStreamIsNotStopped
        paInputOverflowed
        paOutputUnderflowed
        paHostApiNotFound
        paInvalidHostApi
        paCanNotReadFromACallbackStream
        paCanNotWriteToACallbackStream
        paCanNotReadFromAnOutputOnlyStream
        paCanNotWriteToAnInputOnlyStream
        paIncompatibleStreamHostApi
        paBadBufferPtr

    cdef enum PaHostApiTypeId:
        paInDevelopment
        paDirectSound
        paMME
        paASIO
        paSoundManager
        paCoreAudio
        paOSS
        paALSA
        paAL
        paBeOS
        paWDMKS
        paJACK
        paWASAPI
        paAudioScienceHPI

    cdef enum PaStreamCallbackResult:
        paContinue
        paComplete
        paAbort

    int Pa_GetVersion()

    char* Pa_GetVersionText()

    cdef struct PaVersionInfo:
        int versionMajor
        int versionMinor
        int versionSubMinor
        char* versionControlRevision
        char* versionText

    PaVersionInfo* Pa_GetVersionInfo()

    char* Pa_GetErrorText(PaError errorCode)

    PaError Pa_Initialize()

    PaError Pa_Terminate()

    PaHostApiIndex Pa_GetHostApiCount()

    PaHostApiIndex Pa_GetDefaultHostApi()

    cdef struct PaHostApiInfo:
        int structVersion
        PaHostApiTypeId type
        char* name
        int deviceCount
        PaDeviceIndex defaultInputDevice
        PaDeviceIndex defaultOutputDevice

    PaHostApiInfo* Pa_GetHostApiInfo(PaHostApiIndex hostApi)

    PaHostApiIndex Pa_HostApiTypeIdToHostApiIndex(PaHostApiTypeId type)

    PaDeviceIndex Pa_HostApiDeviceIndexToDeviceIndex(PaHostApiIndex hostApi, int hostApiDeviceIndex)

    cdef struct PaHostErrorInfo:
        PaHostApiTypeId hostApiType
        long errorCode
        char* errorText

    PaHostErrorInfo* Pa_GetLastHostErrorInfo()

    PaDeviceIndex Pa_GetDeviceCount()

    PaDeviceIndex Pa_GetDefaultInputDevice()

    PaDeviceIndex Pa_GetDefaultOutputDevice()

    cdef struct PaDeviceInfo:
        int structVersion
        char* name
        PaHostApiIndex hostApi
        int maxInputChannels
        int maxOutputChannels
        PaTime defaultLowInputLatency
        PaTime defaultLowOutputLatency
        PaTime defaultHighInputLatency
        PaTime defaultHighOutputLatency
        double defaultSampleRate

    PaDeviceInfo* Pa_GetDeviceInfo(PaDeviceIndex device)

    cdef struct PaStreamParameters:
        PaDeviceIndex device
        int channelCount
        PaSampleFormat sampleFormat
        PaTime suggestedLatency
        void* hostApiSpecificStreamInfo

    PaError Pa_IsFormatSupported(PaStreamParameters* inputParameters, PaStreamParameters* outputParameters, double sampleRate)

    ctypedef void PaStream

    cdef struct PaStreamCallbackTimeInfo:
        PaTime inputBufferAdcTime
        PaTime currentTime
        PaTime outputBufferDacTime

    ctypedef int PaStreamCallback(void* input, void* output, unsigned long frameCount, PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlags, void* userData)

    PaError Pa_OpenStream(PaStream** stream, PaStreamParameters* inputParameters, PaStreamParameters* outputParameters, double sampleRate, unsigned long framesPerBuffer, PaStreamFlags streamFlags, PaStreamCallback* streamCallback, void* userData)

    PaError Pa_OpenDefaultStream(PaStream** stream, int numInputChannels, int numOutputChannels, PaSampleFormat sampleFormat, double sampleRate, unsigned long framesPerBuffer, PaStreamCallback* streamCallback, void* userData)

    PaError Pa_CloseStream(PaStream* stream)

    ctypedef void PaStreamFinishedCallback(void* userData)

    PaError Pa_SetStreamFinishedCallback(PaStream* stream, PaStreamFinishedCallback* streamFinishedCallback)

    PaError Pa_StartStream(PaStream* stream)

    PaError Pa_StopStream(PaStream* stream)

    PaError Pa_AbortStream(PaStream* stream)

    PaError Pa_IsStreamStopped(PaStream* stream)

    PaError Pa_IsStreamActive(PaStream* stream)

    cdef struct PaStreamInfo:
        int structVersion
        PaTime inputLatency
        PaTime outputLatency
        double sampleRate

    PaStreamInfo* Pa_GetStreamInfo(PaStream* stream)

    PaTime Pa_GetStreamTime(PaStream* stream)

    double Pa_GetStreamCpuLoad(PaStream* stream)

    PaError Pa_ReadStream(PaStream* stream, void* buffer, unsigned long samples)

    PaError Pa_WriteStream(PaStream* stream, void* buffer, unsigned long samples)

    signed long Pa_GetStreamReadAvailable(PaStream* stream)

    signed long Pa_GetStreamWriteAvailable(PaStream* stream)

    PaError Pa_GetSampleSize(PaSampleFormat format)

    void Pa_Sleep(long msec)


cdef class Nothing:
    pass


cdef unsigned long set_flag(unsigned long flags, bint enabled, unsigned long flag) nogil