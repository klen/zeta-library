from os import path as op, environ, getcwd


VERSION = '0.5.93'
BASEDIR = op.abspath(op.dirname(__file__))
LIBDIR = op.join(BASEDIR, 'libs')
CUSTOMDIR = environ.get('ZETA_LIBDIR', None)
FORMATS = ['css', 'scss', 'js']
CURRENT_CONFIG = op.join(getcwd(), "zeta.ini")
HOME_CONFIG = op.join(environ.get('HOME', ''), "zeta.ini")
COLORS = dict(
    okgreen='\033[92m',
    warning='\033[93m',
    fail='\033[91m',
    endc='\033[0m',
)
