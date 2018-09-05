import sys
import argparse

# Version
NUM_VERSION = (1, 0)
VERSION = ".".join(str(nv) for nv in NUM_VERSION)
__version__ = VERSION


################################################################################
def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='Configuration File Handle Module for Python. '
                    'It supports varieties of data type such as '
                    'JSON, YAML, PYTHON DICT.')

    parser.add_argument('config_file', help='JSON or YAML Type of config file.')
    parser.add_argument(
        '-s', '--schema', help='print the config file\'s schema',
        action='store_true')

    args = parser.parse_args()

    if not args.config_file:
        sys.stderr.write("No Config File.")
        exit(1)
    return args


################################################################################
def main():
    args = parse_args()
    from .config import Config

    conf = Config(args.config_file)
    if args.schema:
        sys.stdout.write(conf._make_schema(args.config_file))
