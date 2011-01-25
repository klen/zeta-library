import os.path
import re
import urllib2

from scss.parser import Stylecheet

from zetalibrary import ZetaError, ZETALIBDIR


class Parser(object):
    import_re = comment_re = None

    def parse_path(self, path, curdir):
        """ Parse path.
        """
        if path.startswith('http://'):
            return path

        elif path.startswith('zeta://'):
            path = path[7:]
            return os.path.abspath(os.path.normpath(os.path.join(ZETALIBDIR, path)))

        return os.path.abspath(os.path.normpath(os.path.join(curdir, path)))

    def open_path(self, path, basedir):
        """ Read source.
        """
        if path.startswith('http://'):
            name = os.path.basename(path)
            import_path = os.path.join(basedir, name)
            if not os.path.exists(import_path):
                src = urllib2.urlopen(path).read()
                open(import_path, 'w').write(src)

            path = import_path
        return open(path, 'r')

    def parse(self, path, linker):
        try:
            src = self.open_path(path, linker.basedir).read()
        except IOError:
            linker.out("%s: import file '%s' does not exist." % (linker.basedir, path), error=True)
            return ''

        curdir = os.path.abspath(os.path.dirname(path))
        src, tree = self.parse_import(src)
        for child_path in tree:
            child_path = self.parse_path(child_path, curdir)
            if not child_path in linker.imported:
                try:
                    linker.imported.add(child_path)
                    linker.parse_tree(child_path)
                except (OSError, ZetaError):
                    linker.out("%s: import file '%s' does not exist." % (path, child_path), error=True)

        return self.parse_src(src, curdir, linker)

    def parse_import(self, src):
        result = []
        def child(obj):
            result.append(obj.group(1))
        src = self.import_re.sub(child, src)
        return src, result

    def parse_src(self, src, curdir, linker):
        if linker.no_comments:
            src = self.comment_re.sub('', src)
        return src


class CSSParser(Parser):
    import_re = re.compile(r'^\s*@import +url\(\s*["\']?([^\)\'\"]+)["\']?\s*\)\s*;?\s*$', re.MULTILINE)
    comment_re = re.compile(r'/\*(?:[^*]|\*+[^*/])*\*+/')
    comment_template = '/* %s */\n'
    link_re = re.compile(r'url\(\s*["\']?([^\)\'\"]+)["\']?\)')

    def parse_src(self, src, curdir, linker):
        src = super(CSSParser, self).parse_src(src, curdir, linker)
        def links(obj):
            link_path = obj.group(1)
            for ignore in ('data:image', 'http://', 'https://'):
                if link_path.startswith(ignore):
                    return "url(%s)" % link_path
            try:
                url = "url(%s)" % os.path.relpath(os.path.join(curdir, link_path), linker.basedir)
                url = url.replace("\\", "/")
                return url
            except OSError:
                return "url(%s)" % link_path

        return self.link_re.sub(links, src)


class SCSSParser(CSSParser):
    parser = None
    def parse_src(self, src, curdir, linker):
        src = super(SCSSParser, self).parse_src(src, curdir, linker)
        if not self.parser:
            self.parser = Stylecheet()
        return self.parser.parse(src)


class JSParser(Parser):
    import_re = re.compile(r'^require\(\s*[\'\"]([^\'\"]+)[\'\"]\)\s*;?\s*$', re.MULTILINE)
    comment_re = re.compile(r'/\*(?:[^*]|\*+[^*/])*\*+/')
    comment_template = '// %s\n'


PARSERS = dict(css = CSSParser, scss = SCSSParser, js = JSParser,)
