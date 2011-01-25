import os.path
import unittest

from zetalibrary.main import route, get_frameworks


BASEDIR = os.path.realpath(os.path.dirname(__file__))


class TestLinker( unittest.TestCase ):

    def test_route(self):
        folder = os.path.join(BASEDIR, 'zeta')
        css_file = os.path.join(folder, 'main.css')
        js_file = os.path.join(folder, 'main.js')
        result = list(route(folder))
        self.assertTrue(css_file in result)
        self.assertTrue(js_file in result)

    def test_getframework(self):
        frameworks = list(get_frameworks())
        self.assertTrue(len(frameworks))
