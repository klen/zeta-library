#!/usr/bin/env python
import os

from setuptools import setup, find_packages

from zetalinker import VERSION, PROJECT


def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''


META_DATA = dict(
    name=PROJECT,
    version=VERSION,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='Public domain',

    author='Kirill Klenov',
    author_email='horneds@gmail.com',

    url=' http://github.com/klen/zeta-library',

    platforms=('Any'),

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'zeta-link = zetalinker.parse:main',
        ]
    },
)

if __name__ == "__main__":
    setup( **META_DATA )
