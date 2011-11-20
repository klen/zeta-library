import os.path
import unittest

from zetalibrary.packer import Packer


BASEDIR = os.path.realpath(os.path.dirname(__file__))


class FakeArgs():
    def __init__(self):
        self.format = None
        self.prefix = '_'
        self.compress = False

class TestZeta( unittest.TestCase ):

    def test_zeta(self):
        folder = os.path.join(BASEDIR, 'zeta')

        css_file = os.path.join(folder, 'main.css')
        packer = Packer(css_file, FakeArgs())
        packer.pack()
        orig = open(os.path.join(folder, '_main.css.orig')).read()
        test = open(os.path.join(folder, '_main.css')).read()
        self.assertEqual(test, orig)

        js_file = os.path.join(folder, 'main.js')
        packer = Packer(js_file, FakeArgs())
        packer.pack()
        orig = open(os.path.join(folder, '_main.js.orig')).read()
        test = open(os.path.join(folder, '_main.js')).read()
        self.assertEqual(test, orig)
