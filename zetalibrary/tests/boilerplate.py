import os.path
import unittest

from zetalibrary.main import Linker


BASEDIR = os.path.realpath(os.path.dirname(__file__))
TEST_DIR_NAME = 'boilerplate'


class TestFramework(unittest.TestCase):

    def test_framework(self):
        folder = os.path.join(BASEDIR, TEST_DIR_NAME)
        f = os.path.join(folder, 'main.css')
        linker = Linker(f, no_comments=False)
        linker.link()
        orig = open(os.path.join(folder, '__main.css')).read()
        test = open(os.path.join(folder, '_main.css')).read()
        self.assertEqual(test, orig)
