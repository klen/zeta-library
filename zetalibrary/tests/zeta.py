import os.path
import unittest

from zetalibrary.main import Linker


BASEDIR = os.path.realpath(os.path.dirname(__file__))


class TestZeta( unittest.TestCase ):

    def test_zeta(self):
        folder = os.path.join(BASEDIR, 'zeta')

        css_file = os.path.join(folder, 'main.css')
        linker = Linker(css_file, no_comments=False)
        linker.link()
        orig = open(os.path.join(folder, '_main.css.orig')).read()
        test = open(os.path.join(folder, '_main.css')).read()
        self.assertEqual(test, orig)

        js_file = os.path.join(folder, 'main.js')
        linker = Linker(js_file, no_comments=False)
        linker.link()
        orig = open(os.path.join(folder, '_main.js.orig')).read()
        test = open(os.path.join(folder, '_main.js')).read()
        self.assertEqual(test, orig)
