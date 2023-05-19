<p align="center">
  <!-- Python -->
  <a href="https://www.python.org" alt="Python">
      <img src="https://badges.aleen42.com/src/python.svg" />
  </a>
  <!-- Version -->
  <a href="https://badge.fury.io/py/multiprocess"><img src="https://badge.fury.io/py/multiprocess.svg" alt="PyPI version" height="18"></a>
  <!-- Downloads -->
  <a href="https://pepy.tech/project/multiprocess"><img src="https://static.pepy.tech/personalized-badge/multiprocess?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads" alt="Pypi ownload counter"></a>
  <a href="https://anaconda.org/conda-forge/multiprocess"><img src="https://img.shields.io/conda/dn/conda-forge/multiprocess?color=blue&label=conda%20downloads" alt="Conda download counter"></a>
  </a>
</p>
<p align="center">
  <!-- StackOverflow -->
  <a href="https://stackoverflow.com/questions/tagged/multiprocess"><img src="https://img.shields.io/badge/stackoverflow-get%20help-black.svg" alt="StackOverflow help"></a>
  <!-- Donate -->
  <a href="http://www.uqfoundation.org/pages/donate.html"><img src="https://img.shields.io/badge/support-the%20UQ%20Foundation-purple.svg?style=flat&colorA=grey&colorB=purple" alt="Donate"></a>
  </a>
</p>

## ⚡️ Introduction
[`multiprocess`](https://github.com/uqfoundation/multiprocess) is a Python library that provides multiprocessing and multithreading functionalities. 
[`multiprocess`](https://github.com/uqfoundation/multiprocess) extends [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) by providing enhanced serialization through [`dill`](https://github.com/uqfoundation/dill).
[`multiprocess`](https://github.com/uqfoundation/multiprocess) leverages [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) to support the spawning of processes using the API of the Python standard library's [`threading`](https://docs.python.org/3/library/threading.html) module. 
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) has been part of the standard library since Python 2.6.

[`multiprocess`](https://github.com/uqfoundation/multiprocess) is part of [`pathos`](https://github.com/uqfoundation/pathos),  a Python framework for heterogeneous computing.
[`multiprocess`](https://github.com/uqfoundation/multiprocess) is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated. 
A list of known issues is located [here](https://github.com/uqfoundation/multiprocess/issues), with a legacy list maintained [here](https://uqfoundation.github.io/project/pathos/query).

If you are looking for the dev version, click [here](#development-version)

## ✨ Main Features
[`multiprocess`](https://github.com/uqfoundation/multiprocess) enables:

* objects to be transferred between processes using pipes or multi-producer/multi-consumer queues
* objects to be shared between processes using a server process or (for simple data) shared memory

[`multiprocess`](https://github.com/uqfoundation/multiprocess) provides:

* equivalents of all the synchronization primitives in [`threading`](https://docs.python.org/3/library/threading.html)
* a `Pool` class to facilitate submitting tasks to worker processes
* enhanced serialization, using [`dill`](https://github.com/uqfoundation/dill)

## 🔌 Requirements
```bash
python>=3.7
setuptools>=42
dill>=0.3.6
```

For Python 2, a C compiler is required to build the included extension module from source.  
Python 3 and binary installs do not require a C compiler.

## 💾 Installation 
[`multiprocess`](https://github.com/uqfoundation/multiprocess) can be installed with `pip` or `conda`:
```bash
pip install multiprocess
```
```bash
conda install multiprocess
```

## 💡 Basic Usage
The [``multiprocess.Process``](https://multiprocess.readthedocs.io/en/latest/multiprocess.html#module-multiprocess.process) class follows the API of [``threading.Thread``](https://docs.python.org/3/library/threading.html#thread-objects):


```python
from multiprocess import Process, Queue

def f(q):
    q.put('hello world')

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=[q])
    p.start()
    print(q.get())
    p.join()
```

Synchronization primitives like [locks](https://en.wikipedia.org/wiki/Lock_(computer_science)), [semaphores](https://en.wikipedia.org/wiki/Semaphore_(programming)) and [conditions](https://en.wikipedia.org/wiki/Conditional_(computer_programming)) are available:
```python
from multiprocess import Condition

c = Condition()

print(c)
>>> <Condition(<RLock(None, 0)>), 0>

c.acquire()
>>> True

print(c)
>>> <Condition(<RLock(MainProcess, 1)>), 0>
```

One can also use a manager to create shared objects either in shared memory or in a server process:

```python
from multiprocess import Manager

manager = Manager()
l = manager.list(range(10))
l.reverse()

print(l)
>>> [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

print(repr(l))
>>> <Proxy[list] object at 0x00E1B3B0>
```

Tasks can be offloaded to a [pool](https://en.wikipedia.org/wiki/Pool_(computer_science)) of worker processes in various ways:

```python
from multiprocess import Pool

def f(x):
    return x*x

p = Pool(4)
result = p.map_async(f, range(10))
result.get(timeout=1)
```
Output:
```python
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

When [`dill`](https://github.com/uqfoundation/dill) is installed, serialization is extended to most objects:

```python
from multiprocess import Pool

p = Pool(4)
p.map(lambda x: (lambda y:y**2)(x) + x, range(10))
```
Output:
```python
[0, 2, 6, 12, 20, 30, 42, 56, 72, 90]
```

## 📚 Additional Information

You can find [`multiprocess`](https://github.com/uqfoundation/multiprocess) documentation [here](http://multiprocess.rtfd.io).

``multiprocess.tests`` contains scripts that demonstrate how [`multiprocess`](https://github.com/uqfoundation/multiprocess) can be used to leverage multiple processes to execute Python in parallel.
You can run the test suite with ``python -m multiprocess.tests``.

As [`multiprocess`](https://github.com/uqfoundation/multiprocess) conforms to the [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) interface, the examples and documentation found [here](http://docs.python.org/library/multiprocessing.html) also apply to [`multiprocess`](https://github.com/uqfoundation/multiprocess) if one will ``import multiprocess as multiprocessing``.

Examples that demonstrate some basic use cases and benchmarking for Python code in parallel can be found [here](https://github.com/uqfoundation/multiprocess/tree/master/py3.11/examples).

Please feel free to submit a [ticket on GitHub](https://github.com/uqfoundation/multiprocess/issues/new), or ask a question on [StackOverflow](https://stackoverflow.com/users/2379433/mike-mckerns) ([**@Mike McKerns**](https://stackoverflow.com/users/2379433/mike-mckerns)). If you would like to share how you use [`multiprocess`](https://github.com/uqfoundation/multiprocess) in your work, please send an email (to **mmckerns at uqfoundation dot org**).


## 🎓 Citation
If you use [`multiprocess`](https://github.com/uqfoundation/multiprocess) to do research that leads to publication, we ask that you
acknowledge the use of [`multiprocess`](https://github.com/uqfoundation/multiprocess) by citing the following in your publication:

```
M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
"Building a framework for predictive science", Proceedings of
the 10th Python in Science Conference, 2011;
http://arxiv.org/pdf/1202.1056
```
<details>
<summary>BibTeX</summary>

```bibtex
    @inproceedings{McKerns_1,
        author       = {Michael M. McKerns and
                        Leif Strand and
                        Tim Sullivan and
                        Alta Fang and
                        Michael A. G. Aivazis},
        title        = {Building a Framework for Predictive Science},
        booktitle    = {10th Python in Science Conference},
        year         = {2011},
        url          = {http://arxiv.org/pdf/1202.1056}
    }
```
</details>
  
```  
Michael McKerns and Michael Aivazis,
"pathos: a framework for heterogeneous computing", 2010- ;
https://uqfoundation.github.io/project/pathos
```

<details>
<summary>BibTeX</summary>
  
```bibtex
    @misc{McKerns_2,
        author       = {Michael M. McKerns and
                        Michael A. G. Aivazis},
        title        = {pathos: a framework for heterogeneous computing},
        year         = {2010},
        url          = {https://uqfoundation.github.io/project/pathos}
    }
```
</details> 



Please see https://uqfoundation.github.io/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.

## 📄 License
[`multiprocess`](https://github.com/uqfoundation/multiprocess) is distributed under a 3-clause BSD license, and is a fork of [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html).

## Development Version

[![Support](https://img.shields.io/badge/support-the%20UQ%20Foundation-purple.svg?style=flat&colorA=grey&colorB=purple)](http://www.uqfoundation.org/pages/donate.html)
[![Documentation Status](https://readthedocs.org/projects/multiprocess/badge/?version=latest)](https://multiprocess.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/uqfoundation/multiprocess.svg?label=build&logo=travis&branch=master)](https://travis-ci.com/github/uqfoundation/multiprocess)
[![codecov](https://codecov.io/gh/uqfoundation/multiprocess/branch/master/graph/badge.svg)](https://codecov.io/gh/uqfoundation/multiprocess)

You can get the latest development version with all the shiny new features [here](https://github.com/uqfoundation).  
If you have a new contribution, please submit a pull request.
