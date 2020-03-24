import atexit
import signal

from . import configs, exceptions, formats, pa, streams, __version__


__all__ = \
    configs.__all__ \
    + formats.__all__ \
    + exceptions.__all__ \
    + pa.__all__ \
    + streams.__all__ \
    + __version__.__all__

from .configs import *
from .exceptions import *
from .formats import *
from .pa import *
from .streams import *
from .__version__ import *


pa.initialize()


atexit.register(pa.terminate)

for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGABRT):
    signal.signal(sig, pa.terminate)
