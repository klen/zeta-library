import os.path
import unittest

from zetalibrary.main import Linker


BASEDIR = os.path.realpath(os.path.dirname(__file__))


class TestFrameworks(unittest.TestCase):

    folder = os.path.join(BASEDIR, 'frameworks')

    def check_static(self, filename):
        f = os.path.join(self.folder, filename)
        linker = Linker(f, no_comments=False)
        linker.link()
        orig = open(os.path.join(self.folder, '_%s.orig' % filename)).read()
        test = open(os.path.join(self.folder, '_%s' % filename)).read()
        self.assertEqual(test, orig)

    def test_blueprint(self):
        self.check_static('blueprint.css')

    def test_boilerplate(self):
        self.check_static('boilerplate.css')

    def test_jquery(self):
        self.check_static('jquery.js')

    def test_compass(self):
        self.check_static('compass.css')
