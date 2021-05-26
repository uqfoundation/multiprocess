import sys

class AppTestMemory:
    spaceconfig = dict(usemodules=('_multiprocess', 'mmap',
                                   '_rawffi', 'itertools',
                                   'signal', 'select',
                                   'binascii'))
    if sys.platform == 'win32':
        spaceconfig['usemodules'] += ('_cffi_backend',)
    else:
        spaceconfig['usemodules'] += ('fcntl',)

    def test_address_of(self):
        import _multiprocess
        raises(TypeError, _multiprocess.address_of_buffer, None)
        raises(TypeError, _multiprocess.address_of_buffer, "a")

    if sys.platform == "win32":
        test_address_of.dont_track_allocations = True

    def test_mmap_address(self):
        import mmap
        import _multiprocess

        # This is a bit faster than importing ctypes
        import _ctypes
        class c_double(_ctypes._SimpleCData):
            _type_ = "d"
        sizeof_double = _ctypes.sizeof(c_double)

        buf = mmap.mmap(-1, 300)
        buf[0:300] = '\0' * 300

        # Get the address of shared memory
        address, length = _multiprocess.address_of_buffer(buf)
        assert length == 300

        # build a ctypes object from it
        var = c_double.from_address(address)
        assert buf[0:sizeof_double] == '\0' * sizeof_double
        assert var.value == 0

        # check that both objects share the same memory
        var.value = 123.456
        assert buf[0:sizeof_double] != '\0' * sizeof_double
        buf[0:sizeof_double] = '\0' * sizeof_double
        assert var.value == 0
