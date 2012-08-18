from os import path as op


BASEDIR = op.dirname(__file__)


class FakeArgs():
    def __init__(self, format=None, prefix='_', compress=False, directory=None, output=None):
        self.format = format
        self.prefix = prefix
        self.compress = compress
        self.directory = directory
        self.output = output
