#!/usr/bin/env python
import os.path

VERSION_INFO = (0, 3, 92)

__project__ = PROJECT = __name__
__version__ = VERSION = '.'.join(str(i) for i in VERSION_INFO)
__author__ = AUTHOR = "Kirill Klenov <horneds@gmail.com>"
__license__ = LICENSE = "GNU LGPL"

ZETALIBDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zetalib')


class ZetaError( Exception ):
    """ Zeta error.
    """
    def __init__( self, message, linker=None ):
        if linker and len(linker.tree):
            message = "%s: %s" % (linker.tree[-1]['current'], message)
        super( ZetaError, self ).__init__( message )
