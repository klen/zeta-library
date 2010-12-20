#!/usr/bin/env python
import os

from setuptools import setup, find_packages

from zetalibrary import VERSION, PROJECT, LICENSE


def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''

PACKAGE_DATA = []

for root, dirs, files in os.walk( os.path.join( PROJECT, 'zetalib' ) ):
    for filename in files:
        PACKAGE_DATA.append("%s/%s" % ( root[len(PROJECT)+1:], filename ))

META_DATA = dict(
    name=PROJECT,
    version=VERSION,
    license=LICENSE,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=('Any'),

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen/zeta-library',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Software Development :: Code Generators',
    ],

    packages=find_packages(),
    package_data = { '': PACKAGE_DATA, },

    entry_points={
        'console_scripts': [
            'zeta = zetalibrary.main:main',
        ]
    },

    install_requires = [ 'scss' ]
)

if __name__ == "__main__":
    setup( **META_DATA )
