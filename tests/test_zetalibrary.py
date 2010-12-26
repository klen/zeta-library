import os.path
import unittest
import sys


BASEDIR = os.path.realpath(os.path.dirname(__file__))
RESDIR = os.path.join(BASEDIR, 'res')
CSSFILE = os.path.join(RESDIR, 'test.css')
DONECSSFILE = os.path.join(RESDIR, '_test.css')
JSFILE = os.path.join(RESDIR, 'test.js')
DONEJSFILE = os.path.join(RESDIR, '_test.js')
TESTCSSFILE = os.path.join(RESDIR, 'test_css')
TESTJSFILE = os.path.join(RESDIR, 'test_js')

sys.path.insert(0, os.path.dirname(BASEDIR))
from zetalibrary.main import route, Linker


class TestLinker( unittest.TestCase ):

    def testroute(self):
        result = list(route(RESDIR))
        self.assertTrue(CSSFILE in result)
        self.assertTrue(JSFILE in result)
        result = route(CSSFILE)
        self.assertTrue(CSSFILE in result)

    # def testcss(self):
        # linker = Linker(CSSFILE, no_comments=True)
        # linker.link()
        # test = open(TESTCSSFILE).read()
        # test_link = open(DONECSSFILE).read()
        # self.assertEqual(test, test_link)

    # def testjs(self):
        # linker = Linker(JSFILE, no_comments=True)
        # linker.link()
        # test = open(TESTJSFILE).read()
        # test_link = open(DONEJSFILE).read()
        # self.assertEqual(test, test_link)

    def test_blueprint_project(self):
        folder = os.path.join(BASEDIR, 'zeta_project')
        f = os.path.join(folder, 'main.css')
        linker = Linker(f, no_comments=True)
        linker.link()



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLinker)
    unittest.TextTestRunner(verbosity=2).run(suite)
