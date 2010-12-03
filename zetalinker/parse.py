import optparse
import os.path
import re
import sys
import urllib2

BASEDIR = os.path.realpath(os.path.dirname(__file__))
ZETALIBDIR = os.path.join(BASEDIR, 'zetalib')

FORMATS = {
    'css': {
        'import_template': re.compile(r'^\@import +url\(\s*["\']?([^\)\'\"]+)["\']?\s*\)\s*;?\s*$', re.MULTILINE),
        'comment_template': '/* %s */\n',
        'link_parse': re.compile(r'url\(\s*["\']?([^\)\'\"]+)["\']?\)'),
        'link_ignore': ('data:image', 'http://', 'https://'),
    },
    'js': {
        'import_template': re.compile(r'^require\([\'\"]([^\'\"]+)[\'\"]\)\s*;+\s*$', re.MULTILINE),
        'comment_template': '// %s\n',
    }
}


class LinkerError( Exception ):
    def __init__( self, message, parent=None ):
        if parent:
            message = "%s: %s" % (parent, message)
        super( LinkerError, self ).__init__( message )


class Linker( object ):
    """ Link js and css files in to one.
    """

    def __init__(self, path, prefix='_'):
        self.path = path
        self.prefix = prefix
        self.imported = set()
        self.tree = list()
        self.basedir = os.path.relpath( os.path.dirname( path ))
        self.curfile = None

        filetype = os.path.splitext(path)[1][1:] or ''
        try:
            self.params = FORMATS[filetype]
        except KeyError:
            raise LinkerError("Unknow format file: '%s'" % path)

    def link( self ):
        self.out("Packing '%s'." % self.path)
        self.parse_tree(self.path)
        src = ''
        for item in self.tree:
            src += self.params['comment_template'] % "'%(current)s' from '%(parent)s'" % item
            src += item['src']
            src += "\n"

        pack_name = self.prefix + os.path.basename(self.path)
        pack_path = os.path.join(self.basedir, pack_name)
        try:
            open(pack_path, 'w').write(src)
            self.out("Linked file saved as: '%s'." % pack_path)
        except IOError, e:
            raise LinkerError(e)

    def parse_tree( self, path, parent=None ):
        try:
            src = self.open_path(path).read()
        except IOError, e:
            raise LinkerError(e, parent)

        curdir = os.path.relpath(os.path.normpath(os.path.dirname(path)))

        def children( obj ):
            child_path = self.parse_path(obj.group(1), curdir)
            try:
                if child_path in self.imported:
                    self.out("%s: %s already imported." % (path, child_path))
                    return
                self.imported.add(path)
                self.parse_tree(child_path, path)
            except OSError:
                self.out("%s: import file '%s' does not exist." % (path, child_path), error=True)

        src = self.params['import_template'].sub(children, src)

        if self.params.get('link_parse'):
            src = self.link_parse(src, curdir)

        self.tree.append(dict(src=src, parent=parent, current=path))

    def parse_path(self, path, curdir):
        if path.startswith('http://'):
            return path

        elif path.startswith('/'):
            return os.path.relpath(os.path.normpath(os.path.join(self.basedir, path)))

        elif path.startswith('zeta://'):
            path = path[7:]
            return os.path.relpath(os.path.normpath(os.path.join(ZETALIBDIR, path)))

        return os.path.relpath(os.path.normpath(os.path.join(curdir, path)))

    def link_parse(self, src, curdir):
        def parse( obj ):
            link = obj.group(0)
            path = obj.group(1)
            if self.params.get('link_ignore'):
                for ignore in self.params['link_ignore']:
                    if path.startswith(ignore):
                        return link
            try:
                return link.replace(path, os.path.relpath(os.path.join(curdir, path), self.basedir))
            except OSError:
                self.out('Url error: [%s] -- %s' % (curdir, path), error=True)

        return self.params['link_parse'].sub(parse, src)

    def open_path(self, path):
        if path.startswith('http://'):
            name = os.path.basename(path)
            import_path = os.path.join(self.basedir, name)
            if not os.path.exists(import_path):
                src = urllib2.urlopen(path).read()
                open(import_path, 'w').write(src)

            path = import_path
        return open(path, 'r')

    @staticmethod
    def out( message, error=False ):
        pipe = sys.stdout if not error else sys.stderr
        pipe.write("\n  * %s\n" % message)


def route( path, prefix='_' ):
    """ Route files.
    """
    def test_file( filepath ):
        name, ext = os.path.splitext(os.path.basename(filepath))
        filetype = ext[1:]
        return os.path.isfile(filepath) and not name.startswith(prefix) and filetype in FORMATS.keys()

    if os.path.isdir( path ):
        for name in os.listdir(path):
            filepath = os.path.join(path, name)
            if test_file(filepath):
                yield filepath

    elif test_file(filepath):
        yield filepath


def main():

    p = optparse.OptionParser(
        usage="%prog [--prefix PREFIX] FILENAME or DIRNAME",
        description="Parse file or dir, import css, js code and save with prefix.")

    p.add_option(
        '-p', '--prefix', default='_', metavar='PREFIX',
        help="Save result with prefix. Default is '_'.")

    options, args = p.parse_args()
    if len(args) != 1:
        p.error("Wrong number of arguments.")

    path = args[0]
    try:
        assert os.path.exists(path)
    except AssertionError:
        p.error("'%s' does not exist." % args[0])

    for path in route(path, options.prefix):
        try:
            linker = Linker(path, options.prefix)
            linker.link()
        except LinkerError, e:
            p.error(e)
