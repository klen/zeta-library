Zeta library
============

**Zeta library** is a framework allows to create, collect and pack css, scss, js files much easier. Documentation_ during development.

.. image:: https://secure.travis-ci.org/klen/zeta-library.png?branch=develop
    :target: http://travis-ci.org/klen/zeta-library
    :alt: Build Status

.. contents::


Features
========

- Collect **JS** files;
- Collect **CSS** and **SCSS** files in any order;
- Compress output files;
- Parse custom files in support formats;
- Watch files or folders and auto repack static;
- Has included popular js and css frameworks (you can expand);
- And more...


* **CSS import support**::

    @import url(path or http);


* **JS require support**::

    require("path or http");


* **SCSS compile and imports support** See SCSS_ for more information about language::

    @import url(path or http);

    // or Scss style also supported

    @import 'compass/css3'


* **Blueprint css framework** Ex. ::

    @import url(zeta://blueprint.css);


* **Compass scss framework** Ex. ::

    @import url(zeta://compass.scss);

    // or 

    @import 'compass/reset'


* **Boilerrplate framework support** Ex. ::

    @import url(zeta://boilerplate.css);


* **Zeta css, js framework** Ex: ::

    @import url(zeta://zeta.css);

    require("zeta://zeta.js");


Installation
============

**Zeta library** should be installed using pip or setuptools: ::

    pip install zetalibrary

    easy_install zetalibrary


Usage
=====

$zeta ::

    $ zeta help

    usage: zeta [-h] [-v] {pack,watch,shell,libs} ...

    positional arguments:
    {pack,watch,shell,libs}
        pack                Parse file or dir, import css, js code and save with
                            prefix
        watch               Watch directory for changes and auto pack sources
        shell               A helper command to be used for shell integration
        libs                Show zeta libs

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit

    $ zeta pack --help

    usage: zeta pack [-h] [-p PREFIX] [-f FORMAT] [-c] [-d DIRECTORY] [-o OUTPUT]
                    [-s SETUP_FILE]
                    source

    positional arguments:
    source

    optional arguments:
    -h, --help            show this help message and exit
    -p PREFIX, --prefix PREFIX
                            Save packed files with prefix. Default is '_'
    -f FORMAT, --format FORMAT
                            Force format (css, js, ...). By default format parse
                            from file extension
    -c, --compress        Compress packed sources
    -d DIRECTORY, --directory DIRECTORY
                            Add custom directory for search with prefix: 'zeta://'
                            By default $ZETA_LIBDIR
    -o OUTPUT, --output OUTPUT
                            Set output directory path
    -s SETUP_FILE, --setup-file SETUP_FILE
                            Configuration ini file, with 'Zeta' section




Changes
=======

Make sure you`ve read the following document if you are upgrading from previous versions of zetalibrary:

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


#. Parse `/static/main.js` and minify ::

    $ zeta -c /static/main.js

#. Watch directory `/static/` ::
    
    $ zeta watch /static


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

Development of zeta-library happens at github: https://github.com/klen/zeta-library

* klen_ (Kirill Klenov)


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
.. _klen: https://klen.github.com
