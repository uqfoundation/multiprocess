multiprocess
============
better multiprocessing and multithreading in python

About Multiprocess
------------------
``multiprocess`` is a fork of ``multiprocessing``, and is developed as part of ``pathos``: https://github.com/uqfoundation/pathos

``multiprocessing`` is a package for the Python language which supports the
spawning of processes using the API of the standard library's
``threading`` module. ``multiprocessing`` has been distributed in the standard
library since python 2.6.

Features:

* Objects can be transferred between processes using pipes or
  multi-producer/multi-consumer queues.

* Objects can be shared between processes using a server process or
  (for simple data) shared memory.

* Equivalents of all the synchronization primitives in ``threading``
  are available.

* A ``Pool`` class makes it easy to submit tasks to a pool of worker
  processes.


``multiprocess`` is part of ``pathos``, a python framework for heterogeneous computing.
``multiprocess`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of known issues is maintained
at http://trac.mystic.cacr.caltech.edu/project/pathos/query.html, with a public
ticket list at https://github.com/uqfoundation/multiprocess/issues.

NOTE: A C compiler is required to build the included extension module. For python 3.3 and above, a C compiler is suggested, but not required.


Major Changes
-------------
* enhanced serialization, using ``dill``


Current Release
---------------
This version a fork of ``multiprocessing-0.70a1``.

The latest released version of ``multiprocess`` is available from::
    https://pypi.org/project/multiprocess

``multiprocessing`` is distributed under a BSD license.


Development Version
[![Travis Build Status](https://img.shields.io/travis/uqfoundation/multiprocess.svg?label=build&logo=travis&branch=master)](https://travis-ci.org/uqfoundation/multiprocess)
-------------------
You can get the latest development version with all the shiny new features at::
    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Examples
--------
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
----------------
Probably the best way to get started is to look at the documentation at
http://multiprocess.rtfd.io. See ``multiprocess.examples`` for a set of example
scripts. You can also run the test suite with ``python -m multiprocess.tests``.
Please feel free to submit a ticket on github, or ask a question on
stackoverflow (**@Mike McKerns**).  If you would like to share how you use
``multiprocess`` in your work, please post send an email
(to **mmckerns at uqfoundation dot org**).


Citation
--------
If you use ``multiprocess`` to do research that leads to publication, we ask that you
acknowledge use of ``multiprocess`` by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://trac.mystic.cacr.caltech.edu/project/pathos

Please see http://trac.mystic.cacr.caltech.edu/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.

