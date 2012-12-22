
import _portaudio
from portaudio.exceptions import get_exception, NoError

class PortAudio(object):
    """
    Context manager for using PortAudio
    """
    def __enter__(self):
        err = _portaudio.Pa_Initialize()
        try:
            raise get_exception(err)
        except NoError:
            pass
        return self

    def __exit__(self, type, value, traceback):
        err = _portaudio.Pa_Terminate()
        try:
            raise get_exception(err)
        except NoError:
            pass
