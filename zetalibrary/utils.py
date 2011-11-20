from os import path as op, stat, walk, listdir

from zetalibrary.settings import COLORS, FORMATS, LIBDIR


class ZetaError(Exception):
    " Zeta-library error "
    def __init__(self, message, packer=None):
        if packer and packer.tree:
            message = "%s: %s" % (packer.tree[-1][1], message)
        super(ZetaError, self).__init__(message)


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
    for fname in listdir(LIBDIR):
        fpath = op.join(LIBDIR, fname)
        if op.isfile(fpath):
            description, version = open(fpath).readlines()[1:3]
            yield (fname, version, description)





LAST_MTIME = 0


def files_changed(path, prefix):
    " Return True if the files have changed since the last check "
    def file_times(path):
        " Return the last time files have been modified "
        if op.isdir(path):
            for root, dirs, files in walk(path):
                dirs[:] = [x for x in dirs if x[0] != '.']
                for f in files:
                    if not f.startswith(prefix):
                        yield stat(op.join(root, f)).st_mtime
        else:
            yield stat(path).st_mtime

    global LAST_MTIME
    mtime = max(file_times(path))
    if mtime > LAST_MTIME:
        LAST_MTIME = mtime
        return True
    return False
