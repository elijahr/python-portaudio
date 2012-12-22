'''Wrapper for portaudio.h

Generated with:
/usr/local/bin/ctypesgen.py -lportaudio /usr/include/portaudio.h -o _portaudio.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, str):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return int(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, str):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, str):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, str):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, str):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError as e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["portaudio"] = load_library("portaudio")

# 1 libraries
# End libraries

# No modules

# /usr/include/portaudio.h: 57
if hasattr(_libs['portaudio'], 'Pa_GetVersion'):
    Pa_GetVersion = _libs['portaudio'].Pa_GetVersion
    Pa_GetVersion.argtypes = []
    Pa_GetVersion.restype = c_int

# /usr/include/portaudio.h: 63
if hasattr(_libs['portaudio'], 'Pa_GetVersionText'):
    Pa_GetVersionText = _libs['portaudio'].Pa_GetVersionText
    Pa_GetVersionText.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        Pa_GetVersionText.restype = ReturnString
    else:
        Pa_GetVersionText.restype = String
        Pa_GetVersionText.errcheck = ReturnString

PaError = c_int # /usr/include/portaudio.h: 70

enum_PaErrorCode = c_int # /usr/include/portaudio.h: 104

paNoError = 0 # /usr/include/portaudio.h: 104

paNotInitialized = (-10000) # /usr/include/portaudio.h: 104

paUnanticipatedHostError = (paNotInitialized + 1) # /usr/include/portaudio.h: 104

paInvalidChannelCount = (paUnanticipatedHostError + 1) # /usr/include/portaudio.h: 104

paInvalidSampleRate = (paInvalidChannelCount + 1) # /usr/include/portaudio.h: 104

paInvalidDevice = (paInvalidSampleRate + 1) # /usr/include/portaudio.h: 104

paInvalidFlag = (paInvalidDevice + 1) # /usr/include/portaudio.h: 104

paSampleFormatNotSupported = (paInvalidFlag + 1) # /usr/include/portaudio.h: 104

paBadIODeviceCombination = (paSampleFormatNotSupported + 1) # /usr/include/portaudio.h: 104

paInsufficientMemory = (paBadIODeviceCombination + 1) # /usr/include/portaudio.h: 104

paBufferTooBig = (paInsufficientMemory + 1) # /usr/include/portaudio.h: 104

paBufferTooSmall = (paBufferTooBig + 1) # /usr/include/portaudio.h: 104

paNullCallback = (paBufferTooSmall + 1) # /usr/include/portaudio.h: 104

paBadStreamPtr = (paNullCallback + 1) # /usr/include/portaudio.h: 104

paTimedOut = (paBadStreamPtr + 1) # /usr/include/portaudio.h: 104

paInternalError = (paTimedOut + 1) # /usr/include/portaudio.h: 104

paDeviceUnavailable = (paInternalError + 1) # /usr/include/portaudio.h: 104

paIncompatibleHostApiSpecificStreamInfo = (paDeviceUnavailable + 1) # /usr/include/portaudio.h: 104

paStreamIsStopped = (paIncompatibleHostApiSpecificStreamInfo + 1) # /usr/include/portaudio.h: 104

paStreamIsNotStopped = (paStreamIsStopped + 1) # /usr/include/portaudio.h: 104

paInputOverflowed = (paStreamIsNotStopped + 1) # /usr/include/portaudio.h: 104

paOutputUnderflowed = (paInputOverflowed + 1) # /usr/include/portaudio.h: 104

paHostApiNotFound = (paOutputUnderflowed + 1) # /usr/include/portaudio.h: 104

paInvalidHostApi = (paHostApiNotFound + 1) # /usr/include/portaudio.h: 104

paCanNotReadFromACallbackStream = (paInvalidHostApi + 1) # /usr/include/portaudio.h: 104

paCanNotWriteToACallbackStream = (paCanNotReadFromACallbackStream + 1) # /usr/include/portaudio.h: 104

paCanNotReadFromAnOutputOnlyStream = (paCanNotWriteToACallbackStream + 1) # /usr/include/portaudio.h: 104

paCanNotWriteToAnInputOnlyStream = (paCanNotReadFromAnOutputOnlyStream + 1) # /usr/include/portaudio.h: 104

paIncompatibleStreamHostApi = (paCanNotWriteToAnInputOnlyStream + 1) # /usr/include/portaudio.h: 104

paBadBufferPtr = (paIncompatibleStreamHostApi + 1) # /usr/include/portaudio.h: 104

PaErrorCode = enum_PaErrorCode # /usr/include/portaudio.h: 104

# /usr/include/portaudio.h: 110
if hasattr(_libs['portaudio'], 'Pa_GetErrorText'):
    Pa_GetErrorText = _libs['portaudio'].Pa_GetErrorText
    Pa_GetErrorText.argtypes = [PaError]
    if sizeof(c_int) == sizeof(c_void_p):
        Pa_GetErrorText.restype = ReturnString
    else:
        Pa_GetErrorText.restype = String
        Pa_GetErrorText.errcheck = ReturnString

# /usr/include/portaudio.h: 132
if hasattr(_libs['portaudio'], 'Pa_Initialize'):
    Pa_Initialize = _libs['portaudio'].Pa_Initialize
    Pa_Initialize.argtypes = []
    Pa_Initialize.restype = PaError

# /usr/include/portaudio.h: 151
if hasattr(_libs['portaudio'], 'Pa_Terminate'):
    Pa_Terminate = _libs['portaudio'].Pa_Terminate
    Pa_Terminate.argtypes = []
    Pa_Terminate.restype = PaError

PaDeviceIndex = c_int # /usr/include/portaudio.h: 161

PaHostApiIndex = c_int # /usr/include/portaudio.h: 187

# /usr/include/portaudio.h: 199
if hasattr(_libs['portaudio'], 'Pa_GetHostApiCount'):
    Pa_GetHostApiCount = _libs['portaudio'].Pa_GetHostApiCount
    Pa_GetHostApiCount.argtypes = []
    Pa_GetHostApiCount.restype = PaHostApiIndex

# /usr/include/portaudio.h: 210
if hasattr(_libs['portaudio'], 'Pa_GetDefaultHostApi'):
    Pa_GetDefaultHostApi = _libs['portaudio'].Pa_GetDefaultHostApi
    Pa_GetDefaultHostApi.argtypes = []
    Pa_GetDefaultHostApi.restype = PaHostApiIndex

enum_PaHostApiTypeId = c_int # /usr/include/portaudio.h: 240

paInDevelopment = 0 # /usr/include/portaudio.h: 240

paDirectSound = 1 # /usr/include/portaudio.h: 240

paMME = 2 # /usr/include/portaudio.h: 240

paASIO = 3 # /usr/include/portaudio.h: 240

paSoundManager = 4 # /usr/include/portaudio.h: 240

paCoreAudio = 5 # /usr/include/portaudio.h: 240

paOSS = 7 # /usr/include/portaudio.h: 240

paALSA = 8 # /usr/include/portaudio.h: 240

paAL = 9 # /usr/include/portaudio.h: 240

paBeOS = 10 # /usr/include/portaudio.h: 240

paWDMKS = 11 # /usr/include/portaudio.h: 240

paJACK = 12 # /usr/include/portaudio.h: 240

paWASAPI = 13 # /usr/include/portaudio.h: 240

paAudioScienceHPI = 14 # /usr/include/portaudio.h: 240

PaHostApiTypeId = enum_PaHostApiTypeId # /usr/include/portaudio.h: 240

# /usr/include/portaudio.h: 273
class struct_PaHostApiInfo(Structure):
    pass

struct_PaHostApiInfo.__slots__ = [
    'structVersion',
    'type',
    'name',
    'deviceCount',
    'defaultInputDevice',
    'defaultOutputDevice',
]
struct_PaHostApiInfo._fields_ = [
    ('structVersion', c_int),
    ('type', PaHostApiTypeId),
    ('name', String),
    ('deviceCount', c_int),
    ('defaultInputDevice', PaDeviceIndex),
    ('defaultOutputDevice', PaDeviceIndex),
]

PaHostApiInfo = struct_PaHostApiInfo # /usr/include/portaudio.h: 273

# /usr/include/portaudio.h: 289
if hasattr(_libs['portaudio'], 'Pa_GetHostApiInfo'):
    Pa_GetHostApiInfo = _libs['portaudio'].Pa_GetHostApiInfo
    Pa_GetHostApiInfo.argtypes = [PaHostApiIndex]
    Pa_GetHostApiInfo.restype = POINTER(PaHostApiInfo)

# /usr/include/portaudio.h: 307
if hasattr(_libs['portaudio'], 'Pa_HostApiTypeIdToHostApiIndex'):
    Pa_HostApiTypeIdToHostApiIndex = _libs['portaudio'].Pa_HostApiTypeIdToHostApiIndex
    Pa_HostApiTypeIdToHostApiIndex.argtypes = [PaHostApiTypeId]
    Pa_HostApiTypeIdToHostApiIndex.restype = PaHostApiIndex

# /usr/include/portaudio.h: 331
if hasattr(_libs['portaudio'], 'Pa_HostApiDeviceIndexToDeviceIndex'):
    Pa_HostApiDeviceIndexToDeviceIndex = _libs['portaudio'].Pa_HostApiDeviceIndexToDeviceIndex
    Pa_HostApiDeviceIndexToDeviceIndex.argtypes = [PaHostApiIndex, c_int]
    Pa_HostApiDeviceIndexToDeviceIndex.restype = PaDeviceIndex

# /usr/include/portaudio.h: 342
class struct_PaHostErrorInfo(Structure):
    pass

struct_PaHostErrorInfo.__slots__ = [
    'hostApiType',
    'errorCode',
    'errorText',
]
struct_PaHostErrorInfo._fields_ = [
    ('hostApiType', PaHostApiTypeId),
    ('errorCode', c_long),
    ('errorText', String),
]

PaHostErrorInfo = struct_PaHostErrorInfo # /usr/include/portaudio.h: 342

# /usr/include/portaudio.h: 358
if hasattr(_libs['portaudio'], 'Pa_GetLastHostErrorInfo'):
    Pa_GetLastHostErrorInfo = _libs['portaudio'].Pa_GetLastHostErrorInfo
    Pa_GetLastHostErrorInfo.argtypes = []
    Pa_GetLastHostErrorInfo.restype = POINTER(PaHostErrorInfo)

# /usr/include/portaudio.h: 371
if hasattr(_libs['portaudio'], 'Pa_GetDeviceCount'):
    Pa_GetDeviceCount = _libs['portaudio'].Pa_GetDeviceCount
    Pa_GetDeviceCount.argtypes = []
    Pa_GetDeviceCount.restype = PaDeviceIndex

# /usr/include/portaudio.h: 380
if hasattr(_libs['portaudio'], 'Pa_GetDefaultInputDevice'):
    Pa_GetDefaultInputDevice = _libs['portaudio'].Pa_GetDefaultInputDevice
    Pa_GetDefaultInputDevice.argtypes = []
    Pa_GetDefaultInputDevice.restype = PaDeviceIndex

# /usr/include/portaudio.h: 398
if hasattr(_libs['portaudio'], 'Pa_GetDefaultOutputDevice'):
    Pa_GetDefaultOutputDevice = _libs['portaudio'].Pa_GetDefaultOutputDevice
    Pa_GetDefaultOutputDevice.argtypes = []
    Pa_GetDefaultOutputDevice.restype = PaDeviceIndex

PaTime = c_double # /usr/include/portaudio.h: 409

PaSampleFormat = c_ulong # /usr/include/portaudio.h: 433

# /usr/include/portaudio.h: 466
class struct_PaDeviceInfo(Structure):
    pass

struct_PaDeviceInfo.__slots__ = [
    'structVersion',
    'name',
    'hostApi',
    'maxInputChannels',
    'maxOutputChannels',
    'defaultLowInputLatency',
    'defaultLowOutputLatency',
    'defaultHighInputLatency',
    'defaultHighOutputLatency',
    'defaultSampleRate',
]
struct_PaDeviceInfo._fields_ = [
    ('structVersion', c_int),
    ('name', String),
    ('hostApi', PaHostApiIndex),
    ('maxInputChannels', c_int),
    ('maxOutputChannels', c_int),
    ('defaultLowInputLatency', PaTime),
    ('defaultLowOutputLatency', PaTime),
    ('defaultHighInputLatency', PaTime),
    ('defaultHighOutputLatency', PaTime),
    ('defaultSampleRate', c_double),
]

PaDeviceInfo = struct_PaDeviceInfo # /usr/include/portaudio.h: 466

# /usr/include/portaudio.h: 482
if hasattr(_libs['portaudio'], 'Pa_GetDeviceInfo'):
    Pa_GetDeviceInfo = _libs['portaudio'].Pa_GetDeviceInfo
    Pa_GetDeviceInfo.argtypes = [PaDeviceIndex]
    Pa_GetDeviceInfo.restype = POINTER(PaDeviceInfo)

# /usr/include/portaudio.h: 530
class struct_PaStreamParameters(Structure):
    pass

struct_PaStreamParameters.__slots__ = [
    'device',
    'channelCount',
    'sampleFormat',
    'suggestedLatency',
    'hostApiSpecificStreamInfo',
]
struct_PaStreamParameters._fields_ = [
    ('device', PaDeviceIndex),
    ('channelCount', c_int),
    ('sampleFormat', PaSampleFormat),
    ('suggestedLatency', PaTime),
    ('hostApiSpecificStreamInfo', POINTER(None)),
]

PaStreamParameters = struct_PaStreamParameters # /usr/include/portaudio.h: 530

# /usr/include/portaudio.h: 558
if hasattr(_libs['portaudio'], 'Pa_IsFormatSupported'):
    Pa_IsFormatSupported = _libs['portaudio'].Pa_IsFormatSupported
    Pa_IsFormatSupported.argtypes = [POINTER(PaStreamParameters), POINTER(PaStreamParameters), c_double]
    Pa_IsFormatSupported.restype = PaError

PaStream = None # /usr/include/portaudio.h: 584

PaStreamFlags = c_ulong # /usr/include/portaudio.h: 602

# /usr/include/portaudio.h: 648
class struct_PaStreamCallbackTimeInfo(Structure):
    pass

struct_PaStreamCallbackTimeInfo.__slots__ = [
    'inputBufferAdcTime',
    'currentTime',
    'outputBufferDacTime',
]
struct_PaStreamCallbackTimeInfo._fields_ = [
    ('inputBufferAdcTime', PaTime),
    ('currentTime', PaTime),
    ('outputBufferDacTime', PaTime),
]

PaStreamCallbackTimeInfo = struct_PaStreamCallbackTimeInfo # /usr/include/portaudio.h: 648

PaStreamCallbackFlags = c_ulong # /usr/include/portaudio.h: 657

enum_PaStreamCallbackResult = c_int # /usr/include/portaudio.h: 703

paContinue = 0 # /usr/include/portaudio.h: 703

paComplete = 1 # /usr/include/portaudio.h: 703

paAbort = 2 # /usr/include/portaudio.h: 703

PaStreamCallbackResult = enum_PaStreamCallbackResult # /usr/include/portaudio.h: 703

PaStreamCallback = CFUNCTYPE(c_int, c_void_p, c_void_p, c_ulong, POINTER(PaStreamCallbackTimeInfo), PaStreamCallbackFlags, c_void_p) # /usr/include/portaudio.h: 754

# /usr/include/portaudio.h: 816
if hasattr(_libs['portaudio'], 'Pa_OpenStream'):
    Pa_OpenStream = _libs['portaudio'].Pa_OpenStream
    Pa_OpenStream.argtypes = [POINTER(POINTER(PaStream)), POINTER(PaStreamParameters), POINTER(PaStreamParameters), c_double, c_ulong, PaStreamFlags, POINTER(PaStreamCallback), c_void_p]
    Pa_OpenStream.restype = PaError

# /usr/include/portaudio.h: 856
if hasattr(_libs['portaudio'], 'Pa_OpenDefaultStream'):
    Pa_OpenDefaultStream = _libs['portaudio'].Pa_OpenDefaultStream
    Pa_OpenDefaultStream.argtypes = [POINTER(POINTER(PaStream)), c_int, c_int, PaSampleFormat, c_double, c_ulong, POINTER(PaStreamCallback), POINTER(None)]
    Pa_OpenDefaultStream.restype = PaError

# /usr/include/portaudio.h: 869
if hasattr(_libs['portaudio'], 'Pa_CloseStream'):
    Pa_CloseStream = _libs['portaudio'].Pa_CloseStream
    Pa_CloseStream.argtypes = [POINTER(PaStream)]
    Pa_CloseStream.restype = PaError

PaStreamFinishedCallback = CFUNCTYPE(UNCHECKED(None), POINTER(None)) # /usr/include/portaudio.h: 886

# /usr/include/portaudio.h: 907
if hasattr(_libs['portaudio'], 'Pa_SetStreamFinishedCallback'):
    Pa_SetStreamFinishedCallback = _libs['portaudio'].Pa_SetStreamFinishedCallback
    Pa_SetStreamFinishedCallback.argtypes = [POINTER(PaStream), POINTER(PaStreamFinishedCallback)]
    Pa_SetStreamFinishedCallback.restype = PaError

# /usr/include/portaudio.h: 912
if hasattr(_libs['portaudio'], 'Pa_StartStream'):
    Pa_StartStream = _libs['portaudio'].Pa_StartStream
    Pa_StartStream.argtypes = [POINTER(PaStream)]
    Pa_StartStream.restype = PaError

# /usr/include/portaudio.h: 918
if hasattr(_libs['portaudio'], 'Pa_StopStream'):
    Pa_StopStream = _libs['portaudio'].Pa_StopStream
    Pa_StopStream.argtypes = [POINTER(PaStream)]
    Pa_StopStream.restype = PaError

# /usr/include/portaudio.h: 924
if hasattr(_libs['portaudio'], 'Pa_AbortStream'):
    Pa_AbortStream = _libs['portaudio'].Pa_AbortStream
    Pa_AbortStream.argtypes = [POINTER(PaStream)]
    Pa_AbortStream.restype = PaError

# /usr/include/portaudio.h: 939
if hasattr(_libs['portaudio'], 'Pa_IsStreamStopped'):
    Pa_IsStreamStopped = _libs['portaudio'].Pa_IsStreamStopped
    Pa_IsStreamStopped.argtypes = [POINTER(PaStream)]
    Pa_IsStreamStopped.restype = PaError

# /usr/include/portaudio.h: 955
if hasattr(_libs['portaudio'], 'Pa_IsStreamActive'):
    Pa_IsStreamActive = _libs['portaudio'].Pa_IsStreamActive
    Pa_IsStreamActive.argtypes = [POINTER(PaStream)]
    Pa_IsStreamActive.restype = PaError

# /usr/include/portaudio.h: 993
class struct_PaStreamInfo(Structure):
    pass

struct_PaStreamInfo.__slots__ = [
    'structVersion',
    'inputLatency',
    'outputLatency',
    'sampleRate',
]
struct_PaStreamInfo._fields_ = [
    ('structVersion', c_int),
    ('inputLatency', PaTime),
    ('outputLatency', PaTime),
    ('sampleRate', c_double),
]

PaStreamInfo = struct_PaStreamInfo # /usr/include/portaudio.h: 993

# /usr/include/portaudio.h: 1009
if hasattr(_libs['portaudio'], 'Pa_GetStreamInfo'):
    Pa_GetStreamInfo = _libs['portaudio'].Pa_GetStreamInfo
    Pa_GetStreamInfo.argtypes = [POINTER(PaStream)]
    Pa_GetStreamInfo.restype = POINTER(PaStreamInfo)

# /usr/include/portaudio.h: 1027
if hasattr(_libs['portaudio'], 'Pa_GetStreamTime'):
    Pa_GetStreamTime = _libs['portaudio'].Pa_GetStreamTime
    Pa_GetStreamTime.argtypes = [POINTER(PaStream)]
    Pa_GetStreamTime.restype = PaTime

# /usr/include/portaudio.h: 1046
if hasattr(_libs['portaudio'], 'Pa_GetStreamCpuLoad'):
    Pa_GetStreamCpuLoad = _libs['portaudio'].Pa_GetStreamCpuLoad
    Pa_GetStreamCpuLoad.argtypes = [POINTER(PaStream)]
    Pa_GetStreamCpuLoad.restype = c_double

# /usr/include/portaudio.h: 1070
if hasattr(_libs['portaudio'], 'Pa_ReadStream'):
    Pa_ReadStream = _libs['portaudio'].Pa_ReadStream
    Pa_ReadStream.argtypes = [POINTER(PaStream), POINTER(None), c_ulong]
    Pa_ReadStream.restype = PaError

# /usr/include/portaudio.h: 1097
if hasattr(_libs['portaudio'], 'Pa_WriteStream'):
    Pa_WriteStream = _libs['portaudio'].Pa_WriteStream
    Pa_WriteStream.argtypes = [POINTER(PaStream), POINTER(None), c_ulong]
    Pa_WriteStream.restype = PaError

# /usr/include/portaudio.h: 1110
if hasattr(_libs['portaudio'], 'Pa_GetStreamReadAvailable'):
    Pa_GetStreamReadAvailable = _libs['portaudio'].Pa_GetStreamReadAvailable
    Pa_GetStreamReadAvailable.argtypes = [POINTER(PaStream)]
    Pa_GetStreamReadAvailable.restype = c_long

# /usr/include/portaudio.h: 1121
if hasattr(_libs['portaudio'], 'Pa_GetStreamWriteAvailable'):
    Pa_GetStreamWriteAvailable = _libs['portaudio'].Pa_GetStreamWriteAvailable
    Pa_GetStreamWriteAvailable.argtypes = [POINTER(PaStream)]
    Pa_GetStreamWriteAvailable.restype = c_long

# /usr/include/portaudio.h: 1130
if hasattr(_libs['portaudio'], 'Pa_GetStreamHostApiType'):
    Pa_GetStreamHostApiType = _libs['portaudio'].Pa_GetStreamHostApiType
    Pa_GetStreamHostApiType.argtypes = [POINTER(PaStream)]
    Pa_GetStreamHostApiType.restype = PaHostApiTypeId

# /usr/include/portaudio.h: 1141
if hasattr(_libs['portaudio'], 'Pa_GetSampleSize'):
    Pa_GetSampleSize = _libs['portaudio'].Pa_GetSampleSize
    Pa_GetSampleSize.argtypes = [PaSampleFormat]
    Pa_GetSampleSize.restype = PaError

# /usr/include/portaudio.h: 1151
if hasattr(_libs['portaudio'], 'Pa_Sleep'):
    Pa_Sleep = _libs['portaudio'].Pa_Sleep
    Pa_Sleep.argtypes = [c_long]
    Pa_Sleep.restype = None

# /usr/include/portaudio.h: 169
try:
    paNoDevice = (-1)
except:
    pass

# /usr/include/portaudio.h: 177
try:
    paUseHostApiSpecificDeviceSpecification = (-2)
except:
    pass

# /usr/include/portaudio.h: 436
try:
    paFloat32 = 1
except:
    pass

# /usr/include/portaudio.h: 437
try:
    paInt32 = 2
except:
    pass

# /usr/include/portaudio.h: 438
try:
    paInt24 = 4
except:
    pass

# /usr/include/portaudio.h: 439
try:
    paInt16 = 8
except:
    pass

# /usr/include/portaudio.h: 440
try:
    paInt8 = 16
except:
    pass

# /usr/include/portaudio.h: 441
try:
    paUInt8 = 32
except:
    pass

# /usr/include/portaudio.h: 442
try:
    paCustomFormat = 65536
except:
    pass

# /usr/include/portaudio.h: 444
try:
    paNonInterleaved = 2147483648
except:
    pass

# /usr/include/portaudio.h: 534
try:
    paFormatIsSupported = 0
except:
    pass

# /usr/include/portaudio.h: 591
try:
    paFramesPerBufferUnspecified = 0
except:
    pass

# /usr/include/portaudio.h: 605
try:
    paNoFlag = 0
except:
    pass

# /usr/include/portaudio.h: 610
try:
    paClipOff = 1
except:
    pass

# /usr/include/portaudio.h: 615
try:
    paDitherOff = 2
except:
    pass

# /usr/include/portaudio.h: 626
try:
    paNeverDropInput = 4
except:
    pass

# /usr/include/portaudio.h: 634
try:
    paPrimeOutputBuffersUsingStreamCallback = 8
except:
    pass

# /usr/include/portaudio.h: 639
try:
    paPlatformSpecificFlags = 4294901760
except:
    pass

# /usr/include/portaudio.h: 666
try:
    paInputUnderflow = 1
except:
    pass

# /usr/include/portaudio.h: 675
try:
    paInputOverflow = 2
except:
    pass

# /usr/include/portaudio.h: 681
try:
    paOutputUnderflow = 4
except:
    pass

# /usr/include/portaudio.h: 686
try:
    paOutputOverflow = 8
except:
    pass

# /usr/include/portaudio.h: 692
try:
    paPrimingOutput = 16
except:
    pass

PaHostApiInfo = struct_PaHostApiInfo # /usr/include/portaudio.h: 273

PaHostErrorInfo = struct_PaHostErrorInfo # /usr/include/portaudio.h: 342

PaDeviceInfo = struct_PaDeviceInfo # /usr/include/portaudio.h: 466

PaStreamParameters = struct_PaStreamParameters # /usr/include/portaudio.h: 530

PaStreamCallbackTimeInfo = struct_PaStreamCallbackTimeInfo # /usr/include/portaudio.h: 648

PaStreamInfo = struct_PaStreamInfo # /usr/include/portaudio.h: 993

# No inserted files
