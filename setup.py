#!/usr/bin/env python
from setuptools import setup
import sys

meta = dict(name='portaudio-ctypes',
    version='0.1',
    description='A ctypes-based wrapper around the PortAudio audio I/O library.',
    author='Elijah Rutschman',
    author_email='elijahr@gmail.com',
    license='MIT',
    install_requires=["setuptools"],
    keywords='portaudio',
    url='http://github.com/elijahr/portaudio-ctypes',
    packages=['portaudio'],
)

# Automatic conversion for Python 3 requires distribute.
if False and sys.version_info >= (3,):
    meta.update(dict(
        use_2to3=True,
    ))

setup(**meta)
