import atexit
import signal

from . import buffers, configs, exceptions, formats, pa, streams


__all__ = \
    buffers.__all__ \
    + configs.__all__ \
    + formats.__all__ \
    + exceptions.__all__ \
    + pa.__all__ \
    + streams.__all__

from .buffers import *
from .configs import *
from .exceptions import *
from .formats import *
from .pa import *
from .streams import *


pa.initialize()


atexit.register(pa.terminate)

for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGABRT):
    signal.signal(sig, pa.terminate)
