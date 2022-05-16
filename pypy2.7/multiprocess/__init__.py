#
# Package analogous to 'threading.py' but using processes
#
# multiprocessing/__init__.py
#
# This package is intended to duplicate the functionality (and much of
# the API) of threading.py but uses processes instead of threads.  A
# subpackage 'multiprocessing.dummy' has the same API but is a simple
# wrapper for 'threading'.
#
# Original: Copyright (c) 2006-2008, R Oudkerk
# Original: Licence 3-clause BSD.  The full license text is available at:
# - https://github.com/uqfoundation/multiprocess/blob/master/COPYING.txt
# Forked by Mike McKerns, to support enhanced serialization.

# author, version, license, and long description
__version__ = '0.70.13.dev0'
__author__ = 'Mike McKerns'

__doc__ = """
-----------------------------------------------------------------
multiprocess: better multiprocessing and multithreading in python
-----------------------------------------------------------------

About Multiprocess
====================

``multiprocess`` is a fork of ``multiprocessing``. ``multiprocess`` extends ``multiprocessing`` to provide enhanced serialization, using `dill`. ``multiprocess`` leverages ``multiprocessing`` to support the spawning of processes using the API of the python standard library's ``threading`` module. ``multiprocessing`` has been distributed as part of the standard library since python 2.6.

``multiprocess`` is part of ``pathos``,  a python framework for heterogeneous computing.
``multiprocess`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/multiprocess/issues, with a legacy list maintained at https://uqfoundation.github.io/project/pathos/query.


Major Features
==============

``multiprocess`` enables:

    - objects to be transferred between processes using pipes or multi-producer/multi-consumer queues
    - objects to be shared between processes using a server process or (for simple data) shared memory

``multiprocess`` provides:

    - equivalents of all the synchronization primitives in ``threading``
    - a ``Pool`` class to facilitate submitting tasks to worker processes
    - enhanced serialization, using ``dill``


Current Release
===============

The latest released version of ``multiprocess`` is available from:

    https://pypi.org/project/multiprocess

``multiprocess`` is distributed under a 3-clause BSD license, and is a fork of ``multiprocessing``.


Development Version
===================

You can get the latest development version with all the shiny new features at:

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``multiprocess`` can be installed with ``pip``::

    $ pip install multiprocess

For python 2, a C compiler is required to build the included extension module from source. Python 3 and binary installs do not require a C compiler.


Requirements
============

``multiprocess`` requires:

    - ``python`` (or ``pypy``), **==2.7** or **>=3.7**
    - ``setuptools``, **>=42**
    - ``wheel``, **>=0.1**
    - ``dill``, **>=0.3.4**


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
``multiprocess`` in your work, please send an email (to **mmckerns at uqfoundation dot org**).


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

"""

__license__ = """
Copyright (c) 2008-2016 California Institute of Technology.
Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
All rights reserved.

This software forks the python package "multiprocessing". Licence and
copyright information for multiprocessing can be found in "COPYING.txt".

This software is available subject to the conditions and terms laid
out below. By downloading and using this software you are agreeing
to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the names of the copyright holders nor the names of any of
      the contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

__all__ = [
    'Process', 'current_process', 'active_children', 'freeze_support',
    'Manager', 'Pipe', 'cpu_count', 'log_to_stderr', 'get_logger',
    'allow_connection_pickling', 'BufferTooShort', 'TimeoutError',
    'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Condition',
    'Event', 'Queue', 'JoinableQueue', 'Pool', 'Value', 'Array',
    'RawValue', 'RawArray', 'SUBDEBUG', 'SUBWARNING',
    ]

#
# Imports
#

import os
import sys

from multiprocess.process import Process, current_process, active_children
from multiprocess.util import SUBDEBUG, SUBWARNING

#
# Exceptions
#

class ProcessError(Exception):
    pass

class BufferTooShort(ProcessError):
    pass

class TimeoutError(ProcessError):
    pass

class AuthenticationError(ProcessError):
    pass

# This is down here because _multiprocessing uses BufferTooShort
try:
    import _multiprocess as _multiprocessing
except ImportError:
    import _multiprocessing

#
# Definitions not depending on native semaphores
#

def Manager():
    '''
    Returns a manager associated with a running server process

    The managers methods such as `Lock()`, `Condition()` and `Queue()`
    can be used to create shared objects.
    '''
    from multiprocess.managers import SyncManager
    m = SyncManager()
    m.start()
    return m

def Pipe(duplex=True):
    '''
    Returns two connection object connected by a pipe
    '''
    from multiprocess.connection import Pipe
    return Pipe(duplex)

def cpu_count():
    '''
    Returns the number of CPUs in the system
    '''
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            num = 0
    elif 'bsd' in sys.platform or sys.platform == 'darwin':
        comm = '/sbin/sysctl -n hw.ncpu'
        if sys.platform == 'darwin':
            comm = '/usr' + comm
        try:
            with os.popen(comm) as p:
                num = int(p.read())
        except ValueError:
            num = 0
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            num = 0

    if num >= 1:
        return num
    else:
        raise NotImplementedError('cannot determine number of cpus')

def freeze_support():
    '''
    Check whether this is a fake forked process in a frozen executable.
    If so then run code specified by commandline and exit.
    '''
    if sys.platform == 'win32' and getattr(sys, 'frozen', False):
        from multiprocess.forking import freeze_support
        freeze_support()

def get_logger():
    '''
    Return package logger -- if it does not already exist then it is created
    '''
    from multiprocess.util import get_logger
    return get_logger()

def log_to_stderr(level=None):
    '''
    Turn on logging and add a handler which prints to stderr
    '''
    from multiprocess.util import log_to_stderr
    return log_to_stderr(level)

def allow_connection_pickling():
    '''
    Install support for sending connections and sockets between processes
    '''
    from multiprocess import reduction

#
# Definitions depending on native semaphores
#

def Lock():
    '''
    Returns a non-recursive lock object
    '''
    from multiprocess.synchronize import Lock
    return Lock()

def RLock():
    '''
    Returns a recursive lock object
    '''
    from multiprocess.synchronize import RLock
    return RLock()

def Condition(lock=None):
    '''
    Returns a condition object
    '''
    from multiprocess.synchronize import Condition
    return Condition(lock)

def Semaphore(value=1):
    '''
    Returns a semaphore object
    '''
    from multiprocess.synchronize import Semaphore
    return Semaphore(value)

def BoundedSemaphore(value=1):
    '''
    Returns a bounded semaphore object
    '''
    from multiprocess.synchronize import BoundedSemaphore
    return BoundedSemaphore(value)

def Event():
    '''
    Returns an event object
    '''
    from multiprocess.synchronize import Event
    return Event()

def Queue(maxsize=0):
    '''
    Returns a queue object
    '''
    from multiprocess.queues import Queue
    return Queue(maxsize)

def JoinableQueue(maxsize=0):
    '''
    Returns a queue object
    '''
    from multiprocess.queues import JoinableQueue
    return JoinableQueue(maxsize)

def Pool(processes=None, initializer=None, initargs=(), maxtasksperchild=None):
    '''
    Returns a process pool object
    '''
    from multiprocess.pool import Pool
    return Pool(processes, initializer, initargs, maxtasksperchild)

def RawValue(typecode_or_type, *args):
    '''
    Returns a shared object
    '''
    from multiprocess.sharedctypes import RawValue
    return RawValue(typecode_or_type, *args)

def RawArray(typecode_or_type, size_or_initializer):
    '''
    Returns a shared array
    '''
    from multiprocess.sharedctypes import RawArray
    return RawArray(typecode_or_type, size_or_initializer)

def Value(typecode_or_type, *args, **kwds):
    '''
    Returns a synchronized shared object
    '''
    from multiprocess.sharedctypes import Value
    return Value(typecode_or_type, *args, **kwds)

def Array(typecode_or_type, size_or_initializer, **kwds):
    '''
    Returns a synchronized shared array
    '''
    from multiprocess.sharedctypes import Array
    return Array(typecode_or_type, size_or_initializer, **kwds)

#
#
#

if sys.platform == 'win32':

    def set_executable(executable):
        '''
        Sets the path to a python.exe or pythonw.exe binary used to run
        child processes on Windows instead of sys.executable.
        Useful for people embedding Python.
        '''
        from multiprocess.forking import set_executable
        set_executable(executable)

    __all__ += ['set_executable']
