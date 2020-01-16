import argparse
import datetime

from .presenzialo_web import PRweb
from . import presenzialo_auth as PRauth
from .presenzialo_utils import convert2time, convert2date
from .presenzialo_args import add_parser_debug
from .logs.daylog import DayLog


class PRday:
    def __init__(self, json):

        self.days = []

        r = json["result"]["dettaglio"]

        self._meta = r["meta"]
        self._data = r["data"]

        k_data = r["meta"].index("_dtdata")
        k_timb = r["meta"].index("_jslistatimboriginali")

        for d in r["data"]:
            timbrature = eval(d[k_timb])
            k_orari = timbrature["meta"].index("_iminuti")

            if len(timbrature["data"]) == 0:
                continue

            timbs = [i[k_orari] for i in timbrature["data"]]
            timbs = [convert2time(i).strftime("%H:%M") for i in timbs]

            if len(timbs) % 2 != 0:
                timbs.append(datetime.datetime.now().strftime("%H:%M"))

            d = DayLog(convert2date(d[k_data]), timbs)

            self.days.append(d)


def add_parser_date(parser):

    date_parser = parser.add_argument_group("date options")

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


def main():

    parser = argparse.ArgumentParser(
        prog="PRday",
        description="presenzialo day",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser_date(parser)
    add_parser_debug(parser)

    args = parser.parse_args()

    pr_web = PRweb(PRauth.PRauth(**vars(args)))

    pr_day = PRday(pr_web.timecard(args.day_from, args.day_to))
    for d in pr_day.days:
        print(d)


if __name__ == "__main__":
    main()
