import optparse
import os.path
import sys

from zetalibrary import ZetaError, ZETALIBDIR
from zetalibrary.parsers import PARSERS


COLORS = dict(
    okgreen = '\033[92m',
    warning = '\033[93m',
    fail = '\033[91m',
    endc = '\033[0m',
)


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
        self.basedir = os.path.abspath( os.path.dirname( path ))
        self.parser = None
        self.parsers = dict((k, p()) for k, p  in PARSERS.items())


    def link( self ):
        """ Parse and save file.
        """
        self.out("Packing '%s'." % self.path)
        self.parse_tree(self.path)
        out = ''
        parent = None
        for item in self.tree:
            current = item.get('current', '').replace(ZETALIBDIR, 'zeta:/')
            src = item['src'].strip()
            if not src:
                continue
            out += "".join([
                self.parser.comment_template % ("=" * 30),
                self.parser.comment_template % "Zeta import: '%s'" % current,
                self.parser.comment_template % "From: '%s'" % parent,
                src,
                "\n\n\n",
            ])
            parent = current

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
            self.parser = self.parsers[f.lower()]
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
            alert = '%sError: ' % COLORS['warning']
        pipe.write("\n  *  %s%s\n%s" % (alert,  message, COLORS['endc']))


def get_frameworks():
    path = os.path.join(ZETALIBDIR, 'f')
    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if os.path.isdir(fpath):
            try:
                version = open(os.path.join(fpath, 'version')).read()
                description = open(os.path.join(fpath, 'description')).read()
            except IOError:
                version = description = ''
            yield (fname, version, description)


def get_blocks():
    path = os.path.join(ZETALIBDIR, 'z')
    for bname in os.listdir(path):
        bpath = os.path.join(path, bname)
        if os.path.isdir(bpath):
            yield ( bname, '')



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

    p.add_option(
        '-w', '--show-frameworks', action='store_true', dest='frameworks',
        help="Show available frameworks.")

    p.add_option(
        '-z', '--show-blocks', action='store_true', dest='zeta',
        help="Show available zeta blocks.")

    options, args = p.parse_args()

    if options.frameworks:
        for framework in get_frameworks():
            sys.stdout.write('%s%s%s %s%s\n' % ( COLORS['okgreen'], framework[0], COLORS['endc'], framework[1], framework[2]))
        sys.exit()

    if options.zeta:
        for block in get_blocks():
            sys.stdout.write('%s%s%s%s\n' % ( COLORS['okgreen'], block[0], COLORS['endc'], block[1],))
        sys.exit()

    if len(args) != 1:
        p.print_help(sys.stdout)
        return

    path = args[0]
    try:
        assert os.path.exists(path)
    except AssertionError:
        p.error("%s'%s' does not exist.%s" % (args[0], COLORS['fail'], COLORS['endc']))

    for path in route(path, options.prefix):
        try:
            linker = Linker(path, prefix=options.prefix, no_comments=options.no_comments, format=options.format)
            linker.link()
        except ZetaError, ex:
            p.error("%s%s%s" % (ex, COLORS['fail'], COLORS['warning']))
