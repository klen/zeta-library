#!/usr/bin/env python
import os.path

__project__ = PROJECT = __name__
__version__ = VERSION = "0.2.72"
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
