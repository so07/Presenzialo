import argparse


def add_parser_debug(parser):

    parser.add_argument("--raw", action="store_true", help="raw data")

    parser.add_argument(
        "--debug", "--dry-run", dest="dry_run", action="store_true", help="dry-run mode"
    )
