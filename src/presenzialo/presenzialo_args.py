import argparse
from .presenzialo_config import version


def add_parser_debug(parser):

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + version,
        help="print version information",
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity"
    )

    parser.add_argument(
        "--debug", "--dry-run", dest="dry_run", action="store_true", help="dry-run mode"
    )

    parser.add_argument("--raw", action="store_true", help="raw data")
