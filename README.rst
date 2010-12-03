..   -*- mode: rst -*-

zeta-linker
############

Zeta linker is script for collect js, css files. It's part of zeta-library_.

.. contents::

Requirements
-------------

- python >= 2.5
- pip >= 0.8

Installation
------------

**Zeta linker** should be installed using pip: ::

    pip install git+git://github.com/klen/zeta-linker.git

Usage
------

zeta-link ::

    Usage: zeta-link [--prefix PREFIX] FILENAME or DIRNAME
    Parse file or dir, import css, js code and save with prefix.
    Options:
    -h, --help            show this help message and exit
    -p PREFIX, --prefix=PREFIX Save result with prefix. Default is '_'.

.. _zeta-library: http://github.com/klen/zeta-library.git
