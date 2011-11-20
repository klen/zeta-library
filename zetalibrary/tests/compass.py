import unittest
from os import path as op

from zetalibrary.packer import Packer


BASEDIR = op.dirname(__file__)

class FakeArgs():
    def __init__(self):
        self.format = None
        self.prefix = '_'
        self.compress = False


class TestPacker( unittest.TestCase ):
    folder = op.join(BASEDIR, 'compass')

    def test_pack(self):
        file = op.join(self.folder, 'main.scss')
        Packer(file, FakeArgs()).pack()
        test = open(op.join(self.folder, '_main.scss')).read()
        orig = open(op.join(self.folder, '_main.scss.orig')).read()
        self.assertEqual(test, orig)
