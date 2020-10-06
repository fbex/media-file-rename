import sys
from argparse import ArgumentParser, Namespace

import rename.core
from common import settings


def main():
    args = _parse_arguments()
    settings.VERBOSE_ENABLED = args.verbose
    rename.core.find_and_rename_media_files(args.directory)
    return 0


def _parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description='Rename media files within a directory')
    parser.add_argument('-d', '--directory',
                        metavar='<directory>',
                        type=str,
                        default='.',
                        help='The working directory to use')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
