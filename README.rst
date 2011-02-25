Zeta library
============

**Zeta library** is a framework allows to create, collect and pack css, scss, js files much easier. Documentation_ during development.

.. contents::


Features
========
* **CSS import support**::

    @import url(path or http);

* **JS require support**::

    require("path or http");

* **SCSS compile and imports support** See SCSS_ for more information about language::

    @import url(path or http);

* **Compass blueprint scss, css framework** Ex. ::

    @import url( zeta://blueprint.css );
    /* Or */
    @import url( zeta://blueprint/typography.scss );


* **Partial compass framework support** Ex. ::

    @import url( zeta://compass/reset.scss );

* **Boilerrplate framework support** Ex. ::

    @import url( zeta://boilerplate.css );

* **Zeta css, js framework** Ex: ::

    @import url( zeta://zeta.css );

    require( "zeta://zeta.js" );


Requirements
=============
- python >= 2.5
- python-scss_ >= 6.2


Installation
============

**Zeta library** should be installed using pip or setuptools: ::

    pip install zetalibrary

    easy_install zetalibrary


Usage
=====

$zeta ::

    Usage: zeta [--prefix PREFIX] FILENAME or DIRNAME

    Parse file or dir, import css, js code and save with prefix.

    Options:
    -h, --help            show this help message and exit
    -p PREFIX, --prefix=PREFIX
                            Save result with prefix. Default is '_'.
    -f FORMAT, --format=FORMAT
                            Force use this format.
    -n, --no-comments     Clear comments.
    -w, --show-frameworks
                            Show available frameworks.
    -z, --show-blocks     Show available zeta blocks.


Frameworks
===========
Under construction.


Zeta blocks
============
Under construction.


Changes
=======

Make sure you`ve read the following document if you are upgrading from previous versions of makesite:

http://packages.python.org/zetalibrary/changes.html


Examples
==========
#. Parse all static files in directory ''/tmp/static'' with default prefix::

    $> ls -la /tmp/static
    drwxr-xr-x 4 www-data www-data 4096 2011-02-16 15:09 main
    -rw-r--r-- 1 www-data www-data  335 2011-02-16 15:09 main.css
    -rw-r--r-- 1 www-data www-data  343 2011-02-16 15:09 main.js
    -rw-r--r-- 1 www-data www-data    0 2011-02-16 15:09 print.css

    $> zeta /tmp/static
    ...
    $> ls -la /tmp/static
    drwxr-xr-x 4 www-data www-data 4096 2011-02-16 15:09 main
    -rw-r--r-- 1 www-data www-data  335 2011-02-16 15:09 main.css
    -rw-r--r-- 1 www-data www-data  335 2011-02-16 15:09 _main.css
    -rw-r--r-- 1 www-data www-data  343 2011-02-16 15:09 main.js
    -rw-r--r-- 1 www-data www-data  343 2011-02-16 15:09 _main.js
    -rw-r--r-- 1 www-data www-data    0 2011-02-16 15:09 print.css
    -rw-r--r-- 1 www-data www-data    0 2011-02-16 15:09 _print.css


#. Parse /static/main.js ::

    $> zeta /static/main.js


Options
==========
Under construction.


Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/zeta-library/issues


Contributing
============

Development of python-scss happens at github: https://github.com/klen/zeta-library


License
=======

Licensed under a `GNU lesser general public license`_.


Copyright
=========

Copyright (c) 2011 Kirill Klenov (horneds@gmail.com)

Compass_:
    (c) 2009 Christopher M. Eppstein
    http://compass-style.org/

SCSS_:
    (c) 2006-2009 Hampton Catlin and Nathan Weizenbaum
    http://sass-lang.com/

jQuery_:
    (c) 2009-2010 jQuery Project
    http://jquery.org/


Note
====

**Your feedback are welcome!**

.. _Documentation: http://packages.python.org/zetalibrary/
.. _zeta-library: http://github.com/klen/zeta-library.git
.. _GNU lesser general public license: http://www.gnu.org/copyleft/lesser.html
.. _SCSS: http://sass-lang.com
.. _compass: http://compass-style.org/
.. _jQuery: http://jquery.com
.. _python-scss: http://packages.python.org/scss/
