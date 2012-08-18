import unittest
from os import path as op

from .base import FakeArgs, BASEDIR
from zetalibrary.packer import Packer
from zetalibrary.utils import gen_files, gen_frameworks


class TestPacker(unittest.TestCase):
    folder = op.join(BASEDIR, 'common')

    def test_route(self):
        css_file = op.join(self.folder, 'main.css')
        js_file = op.join(self.folder, 'main.js')
        result = list(gen_files(self.folder))
        self.assertTrue(css_file in result)
        self.assertTrue(js_file in result)

    def test_getframework(self):
        frameworks = list(gen_frameworks())
        self.assertTrue(len(frameworks))

    def test_custom_libs(self):
        js_file = op.join(BASEDIR, 'custom', 'custom.js')
        Packer(js_file, FakeArgs(
            directory=op.join(BASEDIR, 'custom'),
        )).pack()
        self.assertTrue(
            'fake' in open(op.join(BASEDIR, 'custom', '_custom.js')).read())

    def test_pack(self):
        css_file = op.join(self.folder, 'main.css')
        Packer(css_file, FakeArgs(
            output=op.join(BASEDIR, 'common', 'output'),
            compress=True)).pack()
        orig = open(op.join(self.folder, '_main.css.orig')).read()
        test = open(op.join(self.folder, 'output/_main.css')).read()
        self.assertEqual(test, orig)

        js_file = op.join(self.folder, 'main.js')
        Packer(js_file, FakeArgs(
            output=op.join(BASEDIR, 'common', 'output'),
            compress=True)).pack()
        orig = open(op.join(self.folder, '_main.js.orig')).read()
        test = open(op.join(self.folder, 'output/_main.js')).read()
        self.assertEqual(test, orig)
