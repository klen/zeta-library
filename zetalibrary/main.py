import time
import sys
from os import path as op

from argh import ArghParser, command, arg, wrap_errors
from watchdog.observers import Observer

from zetalibrary.settings import BASEDIR, VERSION, CUSTOMDIR
from zetalibrary.utils import ZetaTrick, pack as zeta_pack, gen_frameworks


@command
def shell():
    " A helper command to be used for shell integration "
    print
    print "# Zeta integration "
    print "# ==================== "
    print "source %s" % op.join(BASEDIR, 'shell.sh')
    print


@command
def libs():
    " Show zeta libs "
    for name, description, version, url in gen_frameworks():
        print name
        print ''.join('-' for _ in xrange(len(name)))
        print description.strip('/*\n ')
        print version.strip('/*\n ')
        print url.strip('/*\n ')
        print


@arg('source')
@arg('-p', '--prefix', default="_", help="Save packed files with prefix. Default is '_'")
@arg('-f', '--format', help="Force format (css, js, ...). By default format parse from file extension")
@arg('-c', '--compress', default=False, help="Compress packed sources")
@arg('-d', '--directory', default=CUSTOMDIR, help="Add custom directory for search with prefix: 'zeta://' By default $ZETA_LIBDIR")
@arg('-o', '--output', help="Set output directory path.")
@arg('-s', '--setup-file', help="Configuration ini file")
@wrap_errors(Exception)
def watch(args):
    " Watch directory for changes and auto pack sources "
    assert op.isdir(args.source), "Watch mode allowed only for directories."
    print 'Zeta-library v. %s watch mode' % VERSION
    print '================================'
    print 'Ctrl+C for exit\n'
    observer = Observer()
    handler = ZetaTrick(args=args)
    observer.schedule(handler, args.source, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print "\nWatch mode stoped."
    observer.join()


@arg('source')
@arg('-p', '--prefix', default="_", help="Save packed files with prefix. Default is '_'")
@arg('-f', '--format', help="Force format (css, js, ...). By default format parse from file extension")
@arg('-c', '--compress', default=False, help="Compress packed sources")
@arg('-d', '--directory', default=CUSTOMDIR, help="Add custom directory for search with prefix: 'zeta://' By default $ZETA_LIBDIR")
@arg('-o', '--output', help="Set output directory path")
@arg('-s', '--setup-file', help="Configuration ini file")
@wrap_errors(Exception)
def pack(args):
    " Parse file or dir, import css, js code and save with prefix "
    assert op.exists(args.source), "Does not exists: %s" % args.source
    zeta_pack(args)


def main():
    commands = pack, watch, shell, libs
    names = [f.__name__ for f in commands] + ['help']

    parser = ArghParser()
    parser.add_argument('-v', '--version', action='version',
                        version=VERSION, help='Show zeta version')
    parser.add_commands(commands)
    argv = sys.argv[1:]
    if argv and not argv[0] in names and not argv[0] in ['-v', '--version']:
        argv.insert(0, 'pack')
    parser.dispatch(argv)


if __name__ == "__main__":
    main()
