from argparse import ArgumentParser

_parser = ArgumentParser(description='Rename media files within a directory')
_parser.add_argument('-d', '--directory',
                     metavar='<directory>',
                     type=str,
                     default='',
                     help='The working directory to use')
_parser.add_argument('-v', '--verbose',
                     action='store_true')

args = _parser.parse_args()
