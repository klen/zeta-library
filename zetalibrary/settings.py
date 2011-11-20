from os import path as op, environ


VERSION = '0.5.0'
BASEDIR = op.abspath(op.dirname(__file__))
LIBDIR  = op.join(BASEDIR, 'libs')
CUSTOMDIR = environ.get('ZETA_LIBDIR', None)
FORMATS = ['css', 'scss', 'js']
COLORS = dict(
    okgreen = '\033[92m',
    warning = '\033[93m',
    fail = '\033[91m',
    endc = '\033[0m',
)
