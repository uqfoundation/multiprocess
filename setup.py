#!/usr/bin/env python

import re
import os
import sys
import glob

stable_version = '0.70.12'

# drop support for older python
unsupported = None
if sys.version_info < (2, 7):
    unsupported = 'Versions of Python before 2.7 are not supported'
elif (3, 0) <= sys.version_info < (3, 6):
    unsupported = 'Versions of Python before 3.6 are not supported'
if unsupported:
    raise ValueError(unsupported)

is_jython = sys.platform.startswith('java')
is_pypy = hasattr(sys, 'pypy_version_info')
is_py3k = sys.version_info[0] == 3
lt_py33 = sys.version_info < (3, 3)

# the code is version-specific, so get the appropriate root directory
root = 'pypy' if is_pypy else 'py'
pymajor,pyminor = sys.version_info[:2]
pkgdir = '%s%s.%s' % (root,pymajor,pyminor)
if sys.version_info >= (2, 6):
    pkgname = 'multiprocess'
else: # (2, 5)
    pkgname = 'processing'  #XXX: oddity, due to lazyness at the moment
# if sys.version is higher than explicitly supported, try the latest version
HERE = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(HERE,'%s%s.%s' % (root,pymajor,pyminor))):
    pyminor -= 1
    if pyminor < 0:
        unsupported = 'Python %s is not supported' % pkgdir[len(root):]
        raise ValueError(unsupported)
if '%s%s.%s' % (root,pymajor,pyminor) != pkgdir:
    msg = 'Warning: Python %s is not currently supported, reverting to %s.%s'
    print(msg % (pkgdir[len(root):],pymajor,pyminor))
    pkgdir = '%s%s.%s' % (root,pymajor,pyminor)
srcdir = '%s/Modules/_%s' % (pkgdir, pkgname)
libdir = '%s/%s' % (pkgdir, pkgname)

try:
    from setuptools import setup, Extension, find_packages
    has_setuptools = True
except ImportError:
    from distutils.core import setup, Extension  # noqa
    find_packages = lambda **kwds: [pkgname, pkgname+'.dummy', pkgname+'.tests']
    has_setuptools = False
from distutils import sysconfig
from distutils.errors import CCompilerError, DistutilsExecError, \
                                             DistutilsPlatformError

ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)
if sys.platform == 'win32' and sys.version_info >= (2, 6):
    # distutils.msvc9compiler can raise IOError if the compiler is missing
    ext_errors += (IOError, )

BUILD_WARNING = """

-----------------------------------------------------------------------
WARNING: The C extensions could not be compiled
-----------------------------------------------------------------------

Maybe you do not have a C compiler installed on this system?
The reason was:
%s

This is just a warning as most of the functionality will work even
without the updated C extension.  It will simply fallback to the
built-in _multiprocessing module.  Most notably you will not be able to use
FORCE_EXECV on POSIX systems.  If this is a problem for you then please
install a C compiler or fix the error(s) above.
-----------------------------------------------------------------------

"""

# -*- extra config (setuptools) -*-
if has_setuptools:
    extras = dict(install_requires=['dill>=0.3.4'])
else:
    extras = dict()

# -*- Distribution Meta -*-
here = os.path.abspath(os.path.dirname(__file__))
meta_fh = open(os.path.join(here, '%s/__init__.py' % libdir))
try:
    meta = {}
    for line in meta_fh:
        if line.startswith('__version__'):
            version = line.split()[-1].strip("'").strip('"')
            break
    meta['version'] = version
finally:
    meta_fh.close()

#
# Macros and libraries
#
#   The `macros` dict determines the macros that will be defined when
#   the C extension is compiled.  Each value should be either 0 or 1.
#   (An undefined macro is assumed to have value 0.)  `macros` is only
#   used on Unix platforms.
#
#   The `libraries` dict determines the libraries to which the C
#   extension will be linked.  This should probably be either `['rt']`
#   if you need `librt` or else `[]`.
#
# Meaning of macros
#
#   HAVE_SEM_OPEN
#     Set this to 1 if you have `sem_open()`.  This enables the use of
#     posix named semaphores which are necessary for the
#     implementation of the synchronization primitives on Unix.  If
#     set to 0 then the only way to create synchronization primitives
#     will be via a manager (e.g. "m = Manager(); lock = m.Lock()").
#     
#   HAVE_SEM_TIMEDWAIT
#     Set this to 1 if you have `sem_timedwait()`.  Otherwise polling
#     will be necessary when waiting on a semaphore using a timeout.
#     
#   HAVE_FD_TRANSFER
#     Set this to 1 to compile functions for transferring file
#     descriptors between processes over an AF_UNIX socket using a
#     control message with type SCM_RIGHTS.  On Unix the pickling of 
#     of socket and connection objects depends on this feature.
#
#     If you get errors about missing CMSG_* macros then you should
#     set this to 0.
# 
#   HAVE_BROKEN_SEM_GETVALUE
#     Set to 1 if `sem_getvalue()` does not work or is unavailable.
#     On Mac OSX it seems to return -1 with message "[Errno 78]
#     Function not implemented".
#
#   HAVE_BROKEN_SEM_UNLINK
#     Set to 1 if `sem_unlink()` is unnecessary.  For some reason this
#     seems to be the case on Cygwin where `sem_unlink()` is missing
#     from semaphore.h.
#

if sys.platform == 'win32':  # Windows
    macros = dict()
    libraries = ['ws2_32']
elif sys.platform.startswith('darwin'):  # Mac OSX
    macros = dict(
        HAVE_SEM_OPEN=1,
        HAVE_SEM_TIMEDWAIT=0,
        HAVE_FD_TRANSFER=1,
        HAVE_BROKEN_SEM_GETVALUE=1
        )
    libraries = []
elif sys.platform.startswith('cygwin'):  # Cygwin
    macros = dict(
        HAVE_SEM_OPEN=1,
        HAVE_SEM_TIMEDWAIT=1,
        HAVE_FD_TRANSFER=0,
        HAVE_BROKEN_SEM_UNLINK=1
        )
    libraries = []
elif sys.platform in ('freebsd4', 'freebsd5', 'freebsd6'):
    # FreeBSD's P1003.1b semaphore support is very experimental
    # and has many known problems. (as of June 2008)
    macros = dict(                  # FreeBSD 4-6
        HAVE_SEM_OPEN=0,
        HAVE_SEM_TIMEDWAIT=0,
        HAVE_FD_TRANSFER=1,
        )
    libraries = []
elif re.match('^(gnukfreebsd(8|9|10|11)|freebsd(7|8|9|10))', sys.platform):
    macros = dict(                  # FreeBSD 7+ and GNU/kFreeBSD 8+
        HAVE_SEM_OPEN=bool(
            sysconfig.get_config_var('HAVE_SEM_OPEN') and not
            bool(sysconfig.get_config_var('POSIX_SEMAPHORES_NOT_ENABLED'))
        ),
        HAVE_SEM_TIMEDWAIT=1,
        HAVE_FD_TRANSFER=1,
    )
    libraries = []
elif sys.platform.startswith('openbsd'):
    macros = dict(                  # OpenBSD
        HAVE_SEM_OPEN=0,            # Not implemented
        HAVE_SEM_TIMEDWAIT=0,
        HAVE_FD_TRANSFER=1,
    )
    libraries = []
else:                                   # Linux and other unices
    macros = dict(
        HAVE_SEM_OPEN=1,
        HAVE_SEM_TIMEDWAIT=1,
        HAVE_FD_TRANSFER=1,
    )
    libraries = ['rt']

if sys.platform == 'win32':
    multiprocessing_srcs = [
        '%s/%s.c' % (srcdir, pkgname),
        '%s/semaphore.c' % srcdir,
    ]
    if lt_py33:
        multiprocessing_srcs += [
            '%s/pipe_connection.c' % srcdir,
            '%s/socket_connection.c' % srcdir,
            '%s/win32_functions.c' % srcdir,
        ]
else:
    multiprocessing_srcs = [ '%s/%s.c' % (srcdir, pkgname) ]
    if lt_py33:
        multiprocessing_srcs.append('%s/socket_connection.c' % srcdir)

    if macros.get('HAVE_SEM_OPEN', False):
        multiprocessing_srcs.append('%s/semaphore.c' % srcdir)

long_description = \
'''-----------------------------------------------------------------
multiprocess: better multiprocessing and multithreading in python
-----------------------------------------------------------------

About Multiprocess
====================

``multiprocess`` is a fork of ``multiprocessing``, and is developed as part of ``pathos``: 
https://github.com/uqfoundation/pathos

``multiprocessing`` is a package for the Python language which supports the
spawning of processes using the API of the standard library's
``threading`` module. ``multiprocessing`` has been distributed in the standard
library since python 2.6.

Features:

    - Objects can be transferred between processes using pipes or multi-producer/multi-consumer queues.
    - Objects can be shared between processes using a server process or (for simple data) shared memory.
    - Equivalents of all the synchronization primitives in ``threading`` are available.
    - A ``Pool`` class makes it easy to submit tasks to a pool of worker processes.


``multiprocess`` is part of ``pathos``,  a python framework for heterogeneous computing.
``multiprocess`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/multiprocess/issues, with a legacy list maintained at https://uqfoundation.github.io/project/pathos/query.

NOTE: A C compiler is required to build the included extension module. For python 3.3 and above, a C compiler is suggested, but not required.


Major Changes
==============

    - enhanced serialization, using ``dill``


Current Release
===============

This documentation is for version ``multiprocess-%(thisver)s`` (a fork of ``multiprocessing-0.70a1``).

The latest released version of ``multiprocess`` is available from::

    https://pypi.org/project/multiprocess

``Multiprocessing`` is distributed under a BSD license.


Development Version
===================

You can get the latest development version with all the shiny new features at::

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``multiprocess`` is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf multiprocess-%(relver)s.tgz
    $ cd multiprocess-%(relver)s
    $ python setup.py build
    $ python setup.py install

You will be warned of any missing dependencies and/or settings
after you run the "build" step above.

Alternately, ``multiprocess`` can be installed with ``pip`` or ``easy_install``::

    $ pip install multiprocess

NOTE: A C compiler is required to build the included extension module from source. For python 3.3 and above, a C compiler is suggested, but not required. Binary installs do not require a C compiler.


Requirements
============

``multiprocess`` requires::

    - ``python``, **version == 2.7** or **version >= 3.6**, or ``pypy``
    - ``dill``, **version >= 0.3.4**

Optional requirements::

    - ``setuptools``, **version >= 0.6**


Basic Usage
===========

The ``multiprocess.Process`` class follows the API of ``threading.Thread``.
For example ::

    from multiprocess import Process, Queue

    def f(q):
        q.put('hello world')

    if __name__ == '__main__':
        q = Queue()
        p = Process(target=f, args=[q])
        p.start()
        print (q.get())
        p.join()

Synchronization primitives like locks, semaphores and conditions are
available, for example ::

    >>> from multiprocess import Condition
    >>> c = Condition()
    >>> print (c)
    <Condition(<RLock(None, 0)>), 0>
    >>> c.acquire()
    True
    >>> print (c)
    <Condition(<RLock(MainProcess, 1)>), 0>

One can also use a manager to create shared objects either in shared
memory or in a server process, for example ::

    >>> from multiprocess import Manager
    >>> manager = Manager()
    >>> l = manager.list(range(10))
    >>> l.reverse()
    >>> print (l)
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> print (repr(l))
    <Proxy[list] object at 0x00E1B3B0>

Tasks can be offloaded to a pool of worker processes in various ways,
for example ::

    >>> from multiprocess import Pool
    >>> def f(x): return x*x
    ...
    >>> p = Pool(4)
    >>> result = p.map_async(f, range(10))
    >>> print (result.get(timeout=1))
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

When ``dill`` is installed, serialization is extended to most objects,
for example ::

    >>> from multiprocess import Pool
    >>> p = Pool(4)
    >>> print (p.map(lambda x: (lambda y:y**2)(x) + x, xrange(10)))
    [0, 2, 6, 12, 20, 30, 42, 56, 72, 90]


More Information
================

Probably the best way to get started is to look at the documentation at
http://multiprocess.rtfd.io. See ``multiprocess.examples`` for a set of example
scripts. You can also run the test suite with ``python -m multiprocess.tests``.
Please feel free to submit a ticket on github, or ask a question on
stackoverflow (**@Mike McKerns**).  If you would like to share how you use
``multiprocess`` in your work, please post send an email
(to **mmckerns at uqfoundation dot org**).


Citation
========

If you use ``multiprocess`` to do research that leads to publication, we ask that you
acknowledge use of ``multiprocess`` by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    https://uqfoundation.github.io/project/pathos

Please see https://uqfoundation.github.io/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.
''' % {'relver': stable_version, 'thisver': stable_version}
#long_description = open(os.path.join(HERE, 'README.md')).read()
#long_description += """
#
#===========
#Changes
#===========
#
#"""
#long_description += open(os.path.join(HERE, 'CHANGES.txt')).read()
#if not is_py3k:
#    long_description = long_description.encode('ascii', 'replace')

# -*- Installation Requires -*-
#py_version = sys.version_info
#is_jython = sys.platform.startswith('java')
#is_pypy = hasattr(sys, 'pypy_version_info')

#def strip_comments(l):
#    return l.split('#', 1)[0].strip()
#
#def reqs(f):
#    return list(filter(None, [strip_comments(l) for l in open(
#        os.path.join(os.getcwd(), 'requirements', f)).readlines()]))
#
#if py_version[0] == 3:
#    tests_require = reqs('test3.txt')
#else:
#    tests_require = reqs('test.txt')


def _is_build_command(argv=sys.argv, cmds=('install', 'build', 'bdist')):
    for arg in argv:
        if arg.startswith(cmds):
            return arg


def run_setup(with_extensions=True):
    extensions = []
    if with_extensions:
        extensions = [
            Extension(
                '_%s' % pkgname,
                sources=multiprocessing_srcs,
                define_macros=list(macros.items()),
                libraries=libraries,
                include_dirs=[srcdir],
                depends=glob.glob('%s/*.h' % srcdir) + ['setup.py'],
            ),
        ]
    packages = find_packages(
        where=pkgdir,
        exclude=['ez_setup', 'examples', 'doc',],
        )
    config = dict(
        name='multiprocess',
        version=meta['version'],
        description=('better multiprocessing and multithreading in python'),
        long_description=long_description,
        packages=packages,
        ext_modules=extensions,
        author='Mike McKerns',
        maintainer='Mike McKerns',
        url='https://github.com/uqfoundation/multiprocess',
        download_url='https://github.com/uqfoundation/multiprocess/releases/download/multiprocess-%s/multiprocess-%s.tar.gz' % (stable_version, stable_version),
        zip_safe=False,
        license='BSD',
        package_dir={'': pkgdir},
#       tests_require=tests_require,
#       test_suite='nose.collector',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development',
        ],
        **extras
    )
    setup(**config)

try:
    run_setup(not (is_jython or is_pypy) and lt_py33)
except BaseException:
    if _is_build_command(sys.argv): #XXX: skip WARNING if is_pypy?
        import traceback
        msg = BUILD_WARNING % '\n'.join(traceback.format_stack())
        if not is_py3k:
            exec('print >> sys.stderr, msg')
        else:
            exec('print(msg, file=sys.stderr)')
        run_setup(False)
    else:
        raise
