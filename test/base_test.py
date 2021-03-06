if __name__ == '__main__':
    import sys
    import os
    pkg_dir = os.path.split(os.path.abspath(__file__))[0]
    parent_dir, pkg_name = os.path.split(pkg_dir)
    is_pygame_pkg = (pkg_name == 'tests' and
                     os.path.split(parent_dir)[1] == 'gsdl2')
    if not is_pygame_pkg:
        sys.path.insert(0, parent_dir)
else:
    is_pygame_pkg = __name__.startswith('gsdl2.tests.')

if is_pygame_pkg:
    from gsdl2.tests.test_utils import (
        test_not_implemented, unittest, arrinter, expected_error,
        expected_failure)
else:
    from test.test_utils import (
        test_not_implemented, unittest, arrinter, expected_error,
        expected_failure)
import gsdl2
import sys

init_called = quit_called = 0
def __PYGAMEinit__(): #called automatically by gsdl2.init()
    global init_called
    init_called = init_called + 1
    gsdl2.register_quit(pygame_quit)
def pygame_quit():
    global quit_called
    quit_called = quit_called + 1


quit_hook_ran = 0
def quit_hook():
    global quit_hook_ran
    quit_hook_ran = 1

class BaseModuleTest(unittest.TestCase):
    @expected_failure
    def testAutoInit(self):
        gsdl2.init()
        gsdl2.quit()
        self.assertEqual(init_called, 1)
        self.assertEqual(quit_called, 1)

    def test_get_sdl_byteorder(self):

        # __doc__ (as of 2008-06-25) for gsdl2.base.get_sdl_byteorder:

          # gsdl2.get_sdl_byteorder(): return int
          # get the byte order of SDL

        self.assert_(gsdl2.get_sdl_byteorder() + 1)

    def test_get_sdl_version(self):

        # __doc__ (as of 2008-06-25) for gsdl2.base.get_sdl_version:

          # gsdl2.get_sdl_version(): return major, minor, patch
          # get the version number of SDL

        self.assert_( len(gsdl2.get_sdl_version()) == 3)

    class ExporterBase(object):
        def __init__(self, shape, typechar, itemsize):
            import ctypes

            ndim = len(shape)
            self.ndim = ndim
            self.shape = tuple(shape)
            array_len = 1
            for d in shape:
                array_len *= d
            self.size = itemsize * array_len
            self.parent = ctypes.create_string_buffer(self.size)
            self.itemsize = itemsize
            strides = [itemsize] * ndim
            for i in range(ndim - 1, 0, -1):
                strides[i - 1] = strides[i] * shape[i]
            self.strides = tuple(strides)
            self.data = ctypes.addressof(self.parent), False
            if self.itemsize == 1:
                byteorder = '|'
            elif sys.byteorder == 'big':
                byteorder = '>'
            else:
                byteorder = '<'
            self.typestr = byteorder + typechar + str(self.itemsize)

    def assertSame(self, proxy, obj):
        self.assertEqual(proxy.length, obj.size)
        d = proxy.__array_interface__
        try:
            self.assertEqual(d['typestr'], obj.typestr)
            self.assertEqual(d['shape'], obj.shape)
            self.assertEqual(d['strides'], obj.strides)
            self.assertEqual(d['data'], obj.data)
        finally:
            d = None

    @expected_error(TypeError)
    def test_PgObject_GetBuffer_array_interface(self):
        from gsdl2.bufferproxy import BufferProxy

        class Exporter(self.ExporterBase):
            def get__array_interface__(self):
                return {'version': 3,
                        'typestr': self.typestr,
                        'shape': self.shape,
                        'strides': self.strides,
                        'data': self.data}
            __array_interface__ = property(get__array_interface__)
            # Should be ignored by PgObject_GetBuffer
            __array_struct__ = property(lambda self: None)

        _shape = [2, 3, 5, 7, 11]  # Some prime numbers
        for ndim in range(1, len(_shape)):
            o = Exporter(_shape[0:ndim], 'i', 2)
            v = BufferProxy(o)
            self.assertSame(v, o)
        ndim = 2
        shape = _shape[0:ndim]
        for typechar in ('i', 'u'):
            for itemsize in (1, 2, 4, 8):
                o = Exporter(shape, typechar, itemsize)
                v = BufferProxy(o)
                self.assertSame(v, o)
        for itemsize in (4, 8):
            o = Exporter(shape, 'f', itemsize)
            v = BufferProxy(o)
            self.assertSame(v, o)

        # Is the dict received from an exporting object properly released?
        # The dict should be freed before PgObject_GetBuffer returns.
        # When the BufferProxy v's length property is referenced, v calls
        # PgObject_GetBuffer, which in turn references Exporter2 o's
        # __array_interface__ property. The Exporter2 instance o returns a
        # dict subclass for which it keeps both a regular reference and a
        # weak reference. The regular reference should be the only
        # remaining reference when PgObject_GetBuffer returns. This is
        # verified by first checking the weak reference both before and
        # after the regular reference held by o is removed.

        import weakref, gc

        class NoDictError(RuntimeError):
            pass

        class WRDict(dict):
            """Weak referenceable dict"""
            pass

        class Exporter2(Exporter):
            def get__array_interface__2(self):
                self.d = WRDict(Exporter.get__array_interface__(self))
                self.dict_ref = weakref.ref(self.d)
                return self.d
            __array_interface__ = property(get__array_interface__2)
            def free_dict(self):
                self.d = None
            def is_dict_alive(self):
                try:
                    return self.dict_ref() is not None
                except AttributeError:
                    raise NoDictError("__array_interface__ is unread")

        o = Exporter2((2, 4), 'u', 4)
        v = BufferProxy(o)
        self.assertRaises(NoDictError, o.is_dict_alive)
        length = v.length
        self.assertTrue(o.is_dict_alive())
        o.free_dict()
        gc.collect()
        self.assertFalse(o.is_dict_alive())

    @expected_error(TypeError)
    def test_GetView_array_struct(self):
        from gsdl2.bufferproxy import BufferProxy

        class Exporter(self.ExporterBase):
            def __init__(self, shape, typechar, itemsize):
                super(Exporter, self).__init__(shape, typechar, itemsize)
                self.view = BufferProxy(self.__dict__)

            def get__array_struct__(self):
                return self.view.__array_struct__
            __array_struct__ = property(get__array_struct__)
            # Should not cause PgObject_GetBuffer to fail
            __array_interface__ = property(lambda self: None)

        _shape = [2, 3, 5, 7, 11]  # Some prime numbers
        for ndim in range(1, len(_shape)):
            o = Exporter(_shape[0:ndim], 'i', 2)
            v = BufferProxy(o)
            self.assertSame(v, o)
        ndim = 2
        shape = _shape[0:ndim]
        for typechar in ('i', 'u'):
            for itemsize in (1, 2, 4, 8):
                o = Exporter(shape, typechar, itemsize)
                v = BufferProxy(o)
                self.assertSame(v, o)
        for itemsize in (4, 8):
            o = Exporter(shape, 'f', itemsize)
            v = BufferProxy(o)
            self.assertSame(v, o)

        # Check returned cobject/capsule reference count
        try:
            from sys import getrefcount
        except ImportError:
            # PyPy: no reference counting
            pass
        else:
            o = Exporter(shape, typechar, itemsize)
            self.assertEqual(getrefcount(o.__array_struct__), 1)
 
    if (gsdl2.HAVE_NEWBUF):
        def test_newbuf(self):
            self.NEWBUF_test_newbuf()
        def test_PgDict_AsBuffer_PyBUF_flags(self):
            self.NEWBUF_test_PgDict_AsBuffer_PyBUF_flags()
        def test_PgObject_AsBuffer_PyBUF_flags(self):
            self.NEWBUF_test_PgObject_AsBuffer_PyBUF_flags()
        def test_bad_format(self):
            self.NEWBUF_test_bad_format()
        if is_pygame_pkg:
            from gsdl2.tests.test_utils import buftools
        else:
            from test.test_utils import buftools

    def NEWBUF_assertSame(self, proxy, exp):
        buftools = self.buftools
        Importer = buftools.Importer
        self.assertEqual(proxy.length, exp.len)
        imp = Importer(proxy, buftools.PyBUF_RECORDS_RO)
        try:
            self.assertEqual(imp.readonly, exp.readonly)
            self.assertEqual(imp.format, exp.format)
            self.assertEqual(imp.itemsize, exp.itemsize)
            self.assertEqual(imp.ndim, exp.ndim)
            self.assertEqual(imp.shape, exp.shape)
            self.assertEqual(imp.strides, exp.strides)
            self.assertTrue(imp.suboffsets is None)
        finally:
            imp = None

    def NEWBUF_test_newbuf(self):
        from gsdl2.bufferproxy import BufferProxy

        Exporter = self.buftools.Exporter
        _shape = [2, 3, 5, 7, 11]  # Some prime numbers
        for ndim in range(1, len(_shape)):
            o = Exporter(_shape[0:ndim], '=h')
            v = BufferProxy(o)
            self.NEWBUF_assertSame(v, o)
        ndim = 2
        shape = _shape[0:ndim]
        for format in ['b', 'B', '=h', '=H', '=i', '=I', '=q', '=Q', 'f', 'd',
                       '1h', '=1h', 'x', '1x', '2x', '3x', '4x', '5x', '6x',
                       '7x', '8x', '9x']:
            o = Exporter(shape, format)
            v = BufferProxy(o)
            self.NEWBUF_assertSame(v, o)

    def NEWBUF_test_bad_format(self):
        from gsdl2.bufferproxy import BufferProxy
        from gsdl2.newbuffer import BufferMixin
        from ctypes import create_string_buffer, addressof

        buftools = self.buftools
        Exporter = buftools.Exporter
        Importer = buftools.Importer
        PyBUF_FORMAT = buftools.PyBUF_FORMAT

        for format in ['', '=', '1', ' ', '2h', '=2h',
                       '0x', '11x', '=!', 'h ', ' h', 'hh', '?']:
            exp = Exporter((1,), format, itemsize=2)
            b = BufferProxy(exp)
            self.assertRaises(ValueError, Importer, b, PyBUF_FORMAT)

    def NEWBUF_test_PgDict_AsBuffer_PyBUF_flags(self):
        from gsdl2.bufferproxy import BufferProxy

        is_lil_endian = gsdl2.get_sdl_byteorder() == gsdl2.LIL_ENDIAN
        fsys, frev = ('<', '>') if is_lil_endian else ('>', '<')
        buftools = self.buftools
        Importer = buftools.Importer
        a = BufferProxy({'typestr': '|u4',
                         'shape': (10, 2),
                         'data': (9, False)}) # 9? No data accesses.
        b = Importer(a, buftools.PyBUF_SIMPLE)
        self.assertEqual(b.ndim, 0)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, a.length)
        self.assertEqual(b.itemsize, 4)
        self.assertTrue(b.shape is None)
        self.assertTrue(b.strides is None)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, 9)
        b = Importer(a, buftools.PyBUF_WRITABLE)
        self.assertEqual(b.ndim, 0)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, a.length)
        self.assertEqual(b.itemsize, 4)
        self.assertTrue(b.shape is None)
        self.assertTrue(b.strides is None)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, 9)
        b = Importer(a, buftools.PyBUF_ND)
        self.assertEqual(b.ndim, 2)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, a.length)
        self.assertEqual(b.itemsize, 4)
        self.assertEqual(b.shape, (10, 2))
        self.assertTrue(b.strides is None)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, 9)
        a = BufferProxy({'typestr': fsys + 'i2',
                         'shape': (5, 10),
                         'strides': (24, 2),
                         'data': (42, False)}) # 42? No data accesses.
        b = Importer(a, buftools.PyBUF_STRIDES)
        self.assertEqual(b.ndim, 2)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, 100)
        self.assertEqual(b.itemsize, 2)
        self.assertEqual(b.shape, (5, 10))
        self.assertEqual(b.strides, (24, 2))
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, 42)
        b = Importer(a, buftools.PyBUF_FULL_RO)
        self.assertEqual(b.ndim, 2)
        self.assertEqual(b.format, '=h')
        self.assertEqual(b.len, 100)
        self.assertEqual(b.itemsize, 2)
        self.assertEqual(b.shape, (5, 10))
        self.assertEqual(b.strides, (24, 2))
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, 42)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_SIMPLE)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_ND)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_C_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_F_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_ANY_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_CONTIG)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_SIMPLE)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_ND)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_C_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_F_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_ANY_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_CONTIG)
        a = BufferProxy({'typestr': frev + 'i2',
                         'shape': (3, 5, 10),
                         'strides': (120, 24, 2),
                         'data': (1000000, True)}) # 1000000? No data accesses.
        b = Importer(a, buftools.PyBUF_FULL_RO)
        self.assertEqual(b.ndim, 3)
        self.assertEqual(b.format, frev + 'h')
        self.assertEqual(b.len, 300)
        self.assertEqual(b.itemsize, 2)
        self.assertEqual(b.shape, (3, 5, 10))
        self.assertEqual(b.strides, (120, 24, 2))
        self.assertTrue(b.suboffsets is None)
        self.assertTrue(b.readonly)
        self.assertEqual(b.buf, 1000000)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_FULL)

    def NEWBUF_test_PgObject_AsBuffer_PyBUF_flags(self):
        from gsdl2.bufferproxy import BufferProxy
        import ctypes

        is_lil_endian = gsdl2.get_sdl_byteorder() == gsdl2.LIL_ENDIAN
        fsys, frev = ('<', '>') if is_lil_endian else ('>', '<')
        buftools = self.buftools
        Importer = buftools.Importer
        e = arrinter.Exporter((10, 2), typekind='f',
                              itemsize=ctypes.sizeof(ctypes.c_double))
        a = BufferProxy(e)
        b = Importer(a, buftools.PyBUF_SIMPLE)
        self.assertEqual(b.ndim, 0)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, e.len)
        self.assertEqual(b.itemsize, e.itemsize)
        self.assertTrue(b.shape is None)
        self.assertTrue(b.strides is None)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, e.data)
        b = Importer(a, buftools.PyBUF_WRITABLE)
        self.assertEqual(b.ndim, 0)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, e.len)
        self.assertEqual(b.itemsize, e.itemsize)
        self.assertTrue(b.shape is None)
        self.assertTrue(b.strides is None)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, e.data)
        b = Importer(a, buftools.PyBUF_ND)
        self.assertEqual(b.ndim, e.nd)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, a.length)
        self.assertEqual(b.itemsize, e.itemsize)
        self.assertEqual(b.shape, e.shape)
        self.assertTrue(b.strides is None)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, e.data)
        e = arrinter.Exporter((5, 10), typekind='i', itemsize=2,
                              strides=(24, 2))
        a = BufferProxy(e)
        b = Importer(a, buftools.PyBUF_STRIDES)
        self.assertEqual(b.ndim, e.nd)
        self.assertTrue(b.format is None)
        self.assertEqual(b.len, e.len)
        self.assertEqual(b.itemsize, e.itemsize)
        self.assertEqual(b.shape, e.shape)
        self.assertEqual(b.strides, e.strides)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, e.data)
        b = Importer(a, buftools.PyBUF_FULL_RO)
        self.assertEqual(b.ndim, e.nd)
        self.assertEqual(b.format, '=h')
        self.assertEqual(b.len, e.len)
        self.assertEqual(b.itemsize, e.itemsize)
        self.assertEqual(b.shape, e.shape)
        self.assertEqual(b.strides, e.strides)
        self.assertTrue(b.suboffsets is None)
        self.assertFalse(b.readonly)
        self.assertEqual(b.buf, e.data)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_SIMPLE)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_WRITABLE)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_WRITABLE)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_ND)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_C_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_F_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_ANY_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_CONTIG)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_SIMPLE)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_ND)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_C_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_F_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a,
                          buftools.PyBUF_ANY_CONTIGUOUS)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_CONTIG)
        e = arrinter.Exporter((3, 5, 10), typekind='i', itemsize=2,
                              strides=(120, 24, 2),
                              flags=arrinter.PAI_ALIGNED)
        a = BufferProxy(e)
        b = Importer(a, buftools.PyBUF_FULL_RO)
        self.assertEqual(b.ndim, e.nd)
        self.assertEqual(b.format, frev + 'h')
        self.assertEqual(b.len, e.len)
        self.assertEqual(b.itemsize, e.itemsize)
        self.assertEqual(b.shape, e.shape)
        self.assertEqual(b.strides, e.strides)
        self.assertTrue(b.suboffsets is None)
        self.assertTrue(b.readonly)
        self.assertEqual(b.buf, e.data)
        self.assertRaises(BufferError, Importer, a, buftools.PyBUF_FULL)

    @expected_error(TypeError)
    def test_PgObject_GetBuffer_exception(self):
        # For consistency with surfarray
        from gsdl2.bufferproxy import BufferProxy

        bp = BufferProxy(1)
        self.assertRaises(ValueError, getattr, bp, 'length')

    def not_init_assertions(self):
        self.assert_(not gsdl2.display.get_init(),
                     "display shouldn't be initialized" )
        if 'gsdl2.mixer' in sys.modules:
            self.assert_(not gsdl2.mixer.get_init(),
                         "mixer shouldn't be initialized" )
        if 'gsdl2.font' in sys.modules:
            self.assert_(not gsdl2.font.get_init(),
                         "init shouldn't be initialized" )

        ## !!! TODO : Remove when scrap works for OS X
        import platform
        if platform.system().startswith('Darwin'):
            return

        try:
            self.assertRaises(gsdl2.error, gsdl2.scrap.get)
        except NotImplementedError:
            # Scrap is optional.
            pass

        # gsdl2.cdrom
        # gsdl2.joystick

    def init_assertions(self):
        self.assert_(gsdl2.display.get_init())
        if 'gsdl2.mixer' in sys.modules:
            self.assert_(gsdl2.mixer.get_init())
        if 'gsdl2.font' in sys.modules:
            self.assert_(gsdl2.font.get_init())

    @expected_error(AttributeError)
    def test_quit__and_init(self):
        # __doc__ (as of 2008-06-25) for gsdl2.base.quit:

          # gsdl2.quit(): return None
          # uninitialize all gsdl2 modules

        # Make sure everything is not init
        self.not_init_assertions()

        # Initiate it
        gsdl2.init()

        # Check
        self.init_assertions()

        # Quit
        gsdl2.quit()

        # All modules have quit
        self.not_init_assertions()

    def test_register_quit(self):

        # __doc__ (as of 2008-06-25) for gsdl2.base.register_quit:

          # register_quit(callable): return None
          # register a function to be called when gsdl2 quits

        self.assert_(not quit_hook_ran)

        gsdl2.init()
        gsdl2.register_quit(quit_hook)
        gsdl2.quit()

        self.assert_(quit_hook_ran)


    def test_get_error(self):

        # __doc__ (as of 2008-08-02) for gsdl2.base.get_error:

          # gsdl2.get_error(): return errorstr
          # get the current error message
          #
          # SDL maintains an internal error message. This message will usually
          # be given to you when gsdl2.error is raised. You will rarely need to
          # call this function.
          #

        e = gsdl2.get_error()
        self.assertTrue(e == "" or
                        # This may be returned by SDL_mixer built with
                        # FluidSynth support. Setting environment variable
                        # SDL_SOUNDFONTS to the path of a valid sound font
                        # file removes the error message.
                        e == "No SoundFonts have been requested" or
                        e.startswith("Failed to access the SoundFont"),
                        e)
        gsdl2.set_error("hi")
        self.assertEqual(gsdl2.get_error(), "hi")
        gsdl2.set_error("")
        self.assertEqual(gsdl2.get_error(), "")



    def test_set_error(self):

        e = gsdl2.get_error()
        self.assertTrue(e == "" or
                        # This may be returned by SDL_mixer built with
                        # FluidSynth support. Setting environment variable
                        # SDL_SOUNDFONTS to the path of a valid sf2 file
                        # removes the error message.
                        e == "No SoundFonts have been requested" or
                        e.startswith("Failed to access the SoundFont"),
                        e)
        gsdl2.set_error("hi")
        self.assertEqual(gsdl2.get_error(), "hi")
        gsdl2.set_error("")
        self.assertEqual(gsdl2.get_error(), "")



    @expected_error(AttributeError)
    def test_init(self):

        # __doc__ (as of 2008-08-02) for gsdl2.base.init:

        # gsdl2.init(): return (numpass, numfail)
        # initialize all imported gsdl2 modules
        #
        # Initialize all imported gsdl2 modules. No exceptions will be raised
        # if a module fails, but the total number if successful and failed
        # inits will be returned as a tuple. You can always initialize
        # individual modules manually, but gsdl2.init is a convenient way to
        # get everything started. The init() functions for individual modules
        # will raise exceptions when they fail.
        #
        # You may want to initalise the different modules seperately to speed
        # up your program or to not use things your game does not.
        #
        # It is safe to call this init() more than once: repeated calls will
        # have no effect. This is true even if you have gsdl2.quit() all the
        # modules.
        #



        # Make sure everything is not init
        self.not_init_assertions()

        # Initiate it
        gsdl2.init()

        # Check
        self.init_assertions()

        # Quit
        gsdl2.quit()

        # All modules have quit
        self.not_init_assertions()


    def todo_test_segfault(self):

        # __doc__ (as of 2008-08-02) for gsdl2.base.segfault:

          # crash

        self.fail()

if __name__ == '__main__':
    unittest.main()
