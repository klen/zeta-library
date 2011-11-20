import sys
from argparse import ArgumentParser
from os import path as op

from zetalibrary.packer import Packer
from zetalibrary.settings import BASEDIR
from zetalibrary.utils import color_msg, gen_files, ZetaError


def autocomplete():
    " For shell autocompetion "
    pass


def shell():
    " A helper command to be used for shell integration "
    print
    print "# Zeta integration "
    print "# ==================== "
    print "source %s" % op.join(BASEDIR, 'shell.sh')
    print


def main(args):
    " Parse arguments "
    parser = ArgumentParser(description="Parse file or dir, import css, js code and save with prefix.")
    parser.add_argument('source', help="Path to file or directory")
    parser.add_argument(
        '-p', '--prefix', default='_', dest='prefix',
        help="Save packed files with prefix. Default is '_'.")
    parser.add_argument(
        '-f', '--format', dest='format', help="Force format (css, js, ...). By default format parse from file extension.")
    parser.add_argument(
        '-c', '--compress', dest='compress', action="store_true", help="Compress packed sources")
    args = parser.parse_args()
    try:
        assert op.exists(args.source)
    except AssertionError:
        parser.error(
            color_msg("Does not exists: %s" % args.source, "fail")
        )

    for path in gen_files(args.source, prefix=args.prefix):
        try:
            Packer(path, args).pack()
        except ZetaError, e:
            parser.error(color_msg(str(e), "fail"))


def console():
    autocomplete()
    main(sys.argv[1:])


if __name__ == "__main__":
    main(sys.argv[1:])
