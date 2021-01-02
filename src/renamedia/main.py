import sys
from argparse import ArgumentParser, Namespace

from renamedia.common import settings
from renamedia.rename import core


def main():
    args = _parse_args(sys.argv[1:])
    settings.set_verbose_enabled(args.verbose)
    core.find_and_rename_media_files(args.directory)
    return 0


def _parse_args(args) -> Namespace:
    parser = ArgumentParser(
        description='Rename media files within a directory'
    )
    parser.add_argument(
        '-d', '--directory',
        metavar='<directory>',
        type=str,
        default='.',
        help='The working directory to use'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true'
    )
    return parser.parse_args(args)
