import unittest
from os import path as op

from .base import BASEDIR, FakeArgs
from zetalibrary.packer import Packer


class TestZeta(unittest.TestCase):
    folder = op.join(BASEDIR, 'zeta')

    def test_zeta(self):
        css_file = op.join(self.folder, 'main.css')
        packer = Packer(css_file, FakeArgs())
        packer.pack()
        orig = open(op.join(self.folder, '_main.css.orig')).read()
        test = open(op.join(self.folder, '_main.css')).read()
        self.assertEqual(test, orig)

        js_file = op.join(self.folder, 'main.js')
        packer = Packer(js_file, FakeArgs())
        packer.pack()
        orig = open(op.join(self.folder, '_main.js.orig')).read()
        test = open(op.join(self.folder, '_main.js')).read()
        self.assertEqual(test, orig)
