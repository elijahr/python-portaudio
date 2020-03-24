import argparse
import glob
import itertools
import os
import subprocess
import sys

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install


try:
    import __pypy__
except ImportError:
    __pypy__ = None


BUILD_REQUIRES = {
    'cython<1.0.0': 'from Cython.Build.Dependencies import cythonize',
    'ringbuf>=2.4.0,<3.0.0':  'import ringbuf'
}


for req, imprt in BUILD_REQUIRES.items():
    try:
        exec(imprt)
    except ImportError:
        errno = subprocess.call([sys.executable, '-m', 'pip', 'install', req])
        if errno:
            print('Please install the %s package' % req)
            raise SystemExit(errno)
        else:
            exec(imprt)


DIR = os.path.dirname(__file__)
MODULE_PATH = os.path.join(DIR, 'src', 'portaudio')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--profile', action='store_true')
    parser.add_argument('--annotate-coverage', action='store_true')
    return parser.parse_known_args(sys.argv)[0]


def get_cython_compile_time_env(defaults=None):
    env = dict(**defaults or {})
    env.update({
        'PYPY': __pypy__ is not None
    })
    return env


class BuildExt(build_ext):
    user_options = build_ext.user_options + [
        ('profile', None, 'Build with profiling support'),
        ('annotate-coverage', None, 'Generate coverage annotation xml'),
    ]

    def initialize_options(self):
        super(BuildExt, self).initialize_options()
        args = get_args()
        self.debug = args.debug
        self.profile = args.profile
        self.annotate_coverage = args.annotate_coverage


class Install(install):
    user_options = install.user_options + [
        ('debug', None, 'Build with debug symbols'),
        ('profile', None, 'Build with profiling support'),
        ('annotate-coverage', None, 'Generate coverage annotation xml'),
    ]

    def initialize_options(self):
        super(Install, self).initialize_options()
        args = get_args()
        self.debug = args.debug
        self.profile = args.profile
        self.annotate_coverage = args.annotate_coverage


def get_about():
    about = {}
    with open(os.path.join(MODULE_PATH, '__version__.py'), 'r') as f:
        exec(f.read(), about)
    return about


def get_readme():
    with open("README.md", "r") as fh:
        return fh.read()


def get_packages():
    packages = ['portaudio']
    return packages


def get_package_dir():
    package_dir = {'portaudio': MODULE_PATH}
    return package_dir


def get_package_data():
    package_data = {'portaudio': ['*.pyx', '*.pxd']}
    return package_data


def get_ext_modules():
    args = get_args()
    ext_modules = []
    include_dirs = [DIR, MODULE_PATH]

    for path in itertools.chain(
            glob.glob(os.path.join(MODULE_PATH, '*.pyx'))):
        module_name = path.replace(MODULE_PATH, 'portaudio').replace('/', '.').replace('.pyx', '')
        sources = [path]
        libraries = ['portaudio']
        ext_modules.append(Extension(
            module_name,
            sources=sources,
            libraries=libraries,
            include_dirs=include_dirs,
            language='c++'
        ))

        compile_time_env = get_cython_compile_time_env(
            defaults=dict(
                DEBUG=args.debug,
                CYTHON_TRACE=1 if args.profile else 0,
                CYTHON_TRACE_NOGIL=1 if args.profile else 0))
        ext_modules = cythonize(
            ext_modules,
            gdb_debug=args.debug,
            compile_time_env=compile_time_env,
            annotate=args.annotate_coverage,
            annotate_coverage_xml='coverage.xml' if args.annotate_coverage else None,
            compiler_directives=dict(
                profile=args.profile,
                linetrace=args.profile,
                language_level=3
            ),
        )
    return ext_modules


about = get_about()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    zip_safe=False,
    packages=get_packages(),
    package_dir=get_package_dir(),
    data_files=['README.md', 'LICENSE'],
    package_data=get_package_data(),
    cmdclass={
        'build_ext': BuildExt,
        'install': Install,
    },
    ext_modules=get_ext_modules(),
    install_requires=BUILD_REQUIRES.keys(),
    setup_requires=BUILD_REQUIRES.keys(),
    extras_require={
        'test': [
            'uvloop',
            'pytest',
            'pytest-asyncio',
            'soundfile',
        ],
    },
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Framework :: AsyncIO',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: BSD License',
    ],
)
