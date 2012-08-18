#!/usr/bin/env python
from os import path as op, walk

from setuptools import setup, find_packages

from zetalibrary import VERSION, PROJECT, LICENSE


def read( fname ):
    try:
        return open(op.join(op.dirname( __file__ ), fname)).read()
    except IOError:
        return ''


PACKAGE_DATA = ['shell.sh']
for root, dirs, files in walk(op.join(PROJECT, 'libs')):
    for filename in files:
        PACKAGE_DATA.append("%s/%s" % ( root[len(PROJECT)+1:], filename ))


install_requires = ['cssmin', 'jsmin', 'watchdog', 'argh']
# install_requires = []

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

    install_requires = install_requires,
    test_suite='tests',
)

if __name__ == "__main__":
    setup( **META_DATA )
