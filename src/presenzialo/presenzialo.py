import datetime
import argparse

from .presenzialo_web import PRweb
from .presenzialo_day import PRday
from . import presenzialo_auth as PRauth


def presenzialo(args):

    pr_auth = PRauth.PRauth(**vars(args))
    pr_web = PRweb(pr_auth)

    if args.worker is not None:
        address = pr_web.address_book()
    else:
        pr_day = PRday(pr_web.timecard(args.day_from, args.day_to))
        for d in pr_day.days:
            print(d)


def add_parser_date(parser):

    date_parser = parser.add_argument_group("Date options")

    def _date(s):
        for fmt in ["%Y-%m-%d", "%Y%m%d", "%d-%m-%Y", "%d/%m/%Y"]:
            try:
                return datetime.datetime.strptime(s, fmt).date()
            except:
                pass
        raise ValueError("invalid date {}".format(s))

    date_parser.add_argument(
        "--from",
        dest="day_from",
        type=_date,
        default=datetime.date.today(),  # default=datetime.datetime(1970, 1, 1),
        metavar="YYYY-MM-DD",
        help="from date YYYY-MM-DD",
    )

    date_parser.add_argument(
        "--to",
        dest="day_to",
        type=_date,
        default=datetime.date.today(),
        metavar="YYYY-MM-DD",
        help="to date YYYY-MM-DD (default %(default)s)",
    )


def add_parser_worker(parser):

    parser_group = parser.add_argument_group("Worker options")

    parser_group.add_argument(
        "-i",
        "--in",
        dest="worker",
        metavar="worker",
        default=None,
        help="Worker's presence",
    )


def main():

    parser = argparse.ArgumentParser(
        prog="Presenzialo",
        description="Presenzialo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser_date(parser)
    add_parser_worker(parser)
    PRauth.add_parser(parser)

    args = parser.parse_args()

    presenzialo(args)


if __name__ == "__main__":
    main()
