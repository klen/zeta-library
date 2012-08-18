from os import path as op
import unittest

from .base import BASEDIR, FakeArgs
from zetalibrary.packer import Packer


class LibsTest(unittest.TestCase):
    folder = op.join(BASEDIR, 'libs')

    def test_jquery(self):
        Packer(op.join(self.folder, 'jquery.js'),
               FakeArgs()).pack()
        self.assertEqual(
            open(op.join(self.folder, '_jquery.js')).read(),
            open(op.join(self.folder, '_jquery.js.orig')).read()
        )

    def test_underscore(self):
        Packer(op.join(self.folder, 'underscore.js'),
               FakeArgs()).pack()
        self.assertEqual(
            open(op.join(self.folder, '_underscore.js')).read(),
            open(op.join(self.folder, '_underscore.js.orig')).read()
        )

    def test_blueprint(self):
        Packer(op.join(self.folder, 'blueprint.css'),
               FakeArgs()).pack()
        self.assertEqual(
            open(op.join(self.folder, '_blueprint.css')).read(),
            open(op.join(self.folder, '_blueprint.css.orig')).read()
        )

    def test_boilerplate(self):
        Packer(op.join(self.folder, 'boilerplate.css'),
               FakeArgs()).pack()
        self.assertEqual(
            open(op.join(self.folder, '_boilerplate.css')).read(),
            open(op.join(self.folder, '_boilerplate.css.orig')).read()
        )

    def test_compass(self):
        Packer(op.join(self.folder, 'compass.scss'),
               FakeArgs()).pack()
        self.assertEqual(
            open(op.join(self.folder, '_compass.scss')).read(),
            open(op.join(self.folder, '_compass.scss.orig')).read()
        )
