import os.path
import unittest

from zetalinker import route, Linker


BASEDIR = os.path.realpath(os.path.dirname(__file__))
RESDIR = os.path.join(BASEDIR, 'res')
CSSFILE = os.path.join(RESDIR, 'test.css')
DONECSSFILE = os.path.join(RESDIR, '_test.css')
JSFILE = os.path.join(RESDIR, 'test.js')
DONEJSFILE = os.path.join(RESDIR, '_test.js')
TESTCSSFILE = os.path.join(RESDIR, 'test_css')
TESTJSFILE = os.path.join(RESDIR, 'test_js')


class TestLinker( unittest.TestCase ):

    def testroute( self ):
        result = list(route(RESDIR))
        self.assertTrue(CSSFILE in result)
        self.assertTrue(JSFILE in result)

    def testjs( self ):
        linker = Linker(JSFILE)
        linker.link()
        test = open(TESTJSFILE).read()
        test_link = open(DONEJSFILE).read()
        self.assertEqual(test, test_link)

    def testcss( self ):
        linker = Linker(CSSFILE)
        linker.link()
        test = open(TESTCSSFILE).read()
        test_link = open(DONECSSFILE).read()
        self.assertEqual(test, test_link)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLinker)
    unittest.TextTestRunner(verbosity=2).run(suite)
