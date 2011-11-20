from os import path as op


VERSION = '0.4.24'
BASEDIR = op.abspath(op.dirname(__file__))
LIBDIR  = op.join(BASEDIR, 'libs')
FORMATS = ['css', 'scss', 'js']
COLORS = dict(
    okgreen = '\033[92m',
    warning = '\033[93m',
    fail = '\033[91m',
    endc = '\033[0m',
)
