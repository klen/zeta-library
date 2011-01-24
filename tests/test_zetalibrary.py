import os.path
import unittest
import sys


BASEDIR = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.dirname(BASEDIR))
from zetalibrary.main import route, Linker


class TestLinker( unittest.TestCase ):

    def testroute(self):
        folder = os.path.join(BASEDIR, 'zeta')
        css_file = os.path.join(folder, 'main.css')
        js_file = os.path.join(folder, 'main.js')
        result = list(route(folder))
        self.assertTrue(css_file in result)
        self.assertTrue(js_file in result)

    def test_zeta_project(self):
        """ Test zeta project.
        """
        folder = os.path.join(BASEDIR, 'zeta')
        f = os.path.join(folder, 'main.css')
        linker = Linker(f, no_comments=False)
        linker.link()
        orig = open( os.path.join(folder, '_main.orig') ).read()
        test = open( os.path.join(folder, '_main.css') ).read()
        self.assertEqual(test, orig)

        f = os.path.join(folder, 'main.js')
        linker = Linker(f, no_comments=False)
        linker.link()
        orig = open( os.path.join(folder, '_main.js') ).read()
        test = open( os.path.join(folder, '_main.js.orig') ).read()
        self.assertEqual(test, orig)

    def test_blueprint_project(self):
        """ Test zeta blueprint project.
        """
        folder = os.path.join(BASEDIR, 'blueprint')
        f = os.path.join(folder, 'main.css')
        linker = Linker(f, no_comments=False)
        linker.link()
        orig = open( os.path.join(folder, '_main.orig') ).read()
        test = open( os.path.join(folder, '_main.css') ).read()
        self.assertEqual(test, orig)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLinker)
    unittest.TextTestRunner(verbosity=2).run(suite)
