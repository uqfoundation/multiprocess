import unittest
import __init__ as _test_multiprocessing

_test_multiprocessing.install_tests_in_module_dict(globals(), 'forkserver')

if __name__ == '__main__':
    unittest.main()
