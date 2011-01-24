import optparse
import os.path
import sys

from zetalibrary import ZetaError
from zetalibrary.parsers import PARSERS


class Linker( object ):
    """ Link js and css files in to one.
    """
    def __init__(self, path, **kwargs):
        self.path = path
        self.no_comments = kwargs.get('no_comments')
        self.prefix = kwargs.get('prefix', '_')
        self.format = kwargs.get('format')

        self.imported = set()
        self.tree = list()
        self.basedir = os.path.relpath( os.path.dirname( path ))
        self.parser = None

    def link( self ):
        """ Parse and save file.
        """
        self.out("Packing '%s'." % self.path)
        self.parse_tree(self.path)
        out = ''
        parent = None
        for item in self.tree:
            src = item['src'].strip()
            if not src:
                continue
            out += "".join([
                self.parser.comment_template % ("=" * 30),
                self.parser.comment_template % "Zeta import: '%s'" % item['current'],
                self.parser.comment_template % "From: '%s'" % parent,
                src,
                "\n\n\n",
            ])
            parent = item['current']

        pack_name = self.prefix + os.path.basename(self.path)
        pack_path = os.path.join(self.basedir, pack_name)

        try:
            open(pack_path, 'w').write(out)
            self.out("Linked file saved as: '%s'." % pack_path)
        except IOError, ex:
            raise ZetaError(ex)

    def parse_tree(self, path):
        """ Parse import structure.
        """
        path = path.strip()
        filetype = os.path.splitext(path)[1][1:] or ''
        try:
            f = self.format or filetype
            self.parser = PARSERS[f.lower()]
        except KeyError:
            raise ZetaError("Unknow format file: '%s'" % path)

        src = self.parser.parse(path, self)
        self.tree.append(dict(src=src, current=path))

    @staticmethod
    def out( message, error=False ):
        """ Out messages.
        """
        pipe = sys.stdout
        alert = ''
        if error:
            pipe = sys.stderr
            alert = 'Error: '
        pipe.write("\n  *  %s%s\n" % (alert,  message ))


def route( path, prefix='_' ):
    """ Route files.
    """
    def test_file( filepath ):
        """ Test file is static and not parsed.
        """
        name, ext = os.path.splitext(os.path.basename(filepath))
        filetype = ext[1:].lower()
        return os.path.isfile(filepath) and not name.startswith(prefix) and filetype in PARSERS.keys()

    if os.path.isdir( path ):
        for name in os.listdir(path):
            filepath = os.path.join(path, name)
            if test_file(filepath):
                yield filepath

    elif test_file(path):
        yield path


def main():
    """ Parse arguments.
    """
    p = optparse.OptionParser(
        usage="%prog [--prefix PREFIX] FILENAME or DIRNAME",
        description="Parse file or dir, import css, js code and save with prefix.")

    p.add_option(
        '-p', '--prefix', default='_', dest='prefix',
        help="Save result with prefix. Default is '_'.")

    p.add_option(
        '-f', '--format', dest='format',
        help="Force use this format.")

    p.add_option(
        '-n', '--no-comments', action='store_true', dest='no_comments',
        help="Clear comments.")

    options, args = p.parse_args()
    if len(args) != 1:
        p.print_help(sys.stdout)
        return

    path = args[0]
    try:
        assert os.path.exists(path)
    except AssertionError:
        p.error("'%s' does not exist." % args[0])

    for path in route(path, options.prefix):
        try:
            linker = Linker(path, prefix=options.prefix, no_comments=options.no_comments, format=options.format)
            linker.link()
        except ZetaError, ex:
            p.error(ex)
