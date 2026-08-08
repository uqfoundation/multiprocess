import multiprocess
import os.path
import sys
import unittest
from test import support
import glob
import subprocess as sp
python = sys.executable
try:
    import pox
    python = pox.which_python(version=True) or python
except ImportError:
    pass
shell = sys.platform[:3] == 'win'

if support.PGO:
    raise unittest.SkipTest("test is not helpful for PGO")

if sys.platform == "win32":
    raise unittest.SkipTest("forkserver is not available on Windows")

# The forkserver start method requires passing file descriptors over a Unix
# socket, which is not available on every platform (e.g. Solaris/illumos).
if "forkserver" not in multiprocess.get_all_start_methods():
    raise unittest.SkipTest("forkserver start method is not available")

suite = os.path.dirname(__file__) or os.path.curdir
tests = glob.glob(suite + os.path.sep + 'test_*.py')


if __name__ == '__main__':

    failed = 0
    for test in tests:
        p = sp.Popen([python, test], shell=shell).wait()
        if p:
            failed = 1
    print('')
    exit(failed)
