from os import path as op, listdir

from watchdog.tricks import Trick

from zetalibrary.settings import COLORS, FORMATS, LIBDIR, CURRENT_CONFIG, HOME_CONFIG
from ConfigParser import ConfigParser


def color_msg(msg, color):
    " Return colored message "
    return ''.join((COLORS.get(color, COLORS['endc']), msg, COLORS['endc']))


def is_parsed_file(path, prefix="_"):
    name, ext = op.splitext(op.basename(path))
    return op.isfile(path) and not name.startswith(prefix) and ext[1:].lower() in FORMATS


def gen_files(path, prefix="_"):
    " Return file generator "

    if op.isdir(path):
        for name in listdir(path):
            fpath = op.join(path, name)
            if is_parsed_file(fpath):
                yield op.abspath(fpath)

    elif is_parsed_file(path):
        yield op.abspath(path)


def gen_frameworks():
    for fname in sorted(listdir(LIBDIR)):
        name, ext = op.splitext(fname)
        fpath = op.join(LIBDIR, fname)
        if not name.startswith('_') and op.isfile(fpath) and ext.strip('.') in ['css', 'js', 'scss']:
            description, url, version = open(fpath).readlines()[0:3]
            yield (fname, description, version, url)


def pack(args):
    " Pack files. "
    from zetalibrary.packer import Packer

    args = parse_config(args)
    for path in gen_files(args.source, prefix=args.prefix):
        Packer(path, args).pack()


def parse_config(args):
    parser = ConfigParser()
    parser.add_section('Zeta')
    parser.read([CURRENT_CONFIG, HOME_CONFIG, args.setup_file or ''])
    for k, v in parser._sections['Zeta'].iteritems():
        if getattr(args, k, None) is None:
            setattr(args, k, v)
    return args


class ZetaTrick(Trick):
    " Zeta directory event handler "

    def __init__(self, args=None):
        self.args = args
        self.formats = ['css', 'js', 'scss', args.format]
        super(ZetaTrick, self).__init__()

    def dispatch(self, event):
        name = op.basename(event.src_path)
        _, ext = op.splitext(name)
        if (not name.startswith(self.args.prefix)
                and not event.is_directory
                and ext.lstrip('.').lower() in self.formats):
            super(ZetaTrick, self).dispatch(event)

    def on_any_event(self, event):
        print "\nChanges found: %s" % event.src_path
        pack(self.args)


class ZetaError(Exception):
    " Zeta-library error "
    pass
