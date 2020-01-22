import os
import json
import argparse

from .presenzialo_web import PRweb
from .presenzialo_auth import PRauth
from .presenzialo_config import config_address
from .presenzialo_id import PRworker
from .presenzialo_args import add_parser_debug
from .presenzialo_utils import write_data, read_data

from collections import namedtuple, OrderedDict

Day = namedtuple("Day", "smart_working mission other")

Day.__new__.__defaults__ = (None,) * len(Day._fields)


Worker = namedtuple(
    "Worker", "name id status phone phone2 office group boss today tomorrow"
)

Worker.__new__.__defaults__ = (None,) * len(Worker._fields)


class PRaddress:
    def __init__(self, pr_web, cache=False, raw=False):

        self.pr_web = pr_web
        self.pr_ids = PRworker(pr_web)

        self.workers = OrderedDict()

        self.raw = raw

        self.cache = cache

        if self.cache:
            self.json_address_phone = self.download()
            write_data(self.json_address_phone, config_address)
        else:
            if os.path.isfile(config_address):
                self.json_address_phone = read_data(config_address)
            else:
                self.json_address_phone = {}

        self.address_phone = self.parse(self.json_address_phone)

    def present(self, name):
        if isinstance(name, str):
            name = [name]
        # upper case
        name = [n.upper() for n in name]

        for n in name:
            for i in self.pr_ids.id(n):
                js = self.pr_web.address_book(i)
                d = self.parse(js)

                for k, v in d.items():
                    self.workers[k] = v

        print(self)

        return self.workers

    def parse(self, json):

        if self.raw:
            print(json)

        d = OrderedDict()

        for i in json:

            day = {}
            for k in ["oggi", "domani"]:
                if i[k]:
                    day[k] = Day(i[k]["telelavoro"], i[k]["misstrasf"], i[k]["altro"])

            w = Worker(
                i["nominativo"].strip(),
                i["id"],
                i["descrstato"].strip(),
                i["telefono"].strip(),
                i["libero"].strip(),
                i["altro"],
                i["centrocontr"],
                i["responsabile"],
                day.get("oggi", None),
                day.get("domani", None),
            )

            d[w.id] = w

        return d

    def download(self):
        return self.pr_web.address_book()

    def __str__(self):
        s = ""
        for i, (k, v) in enumerate(self.workers.items()):
            s += "{}\n".format(v.name)
            s += "  {}\n".format(v.status)
            s += "  {} {}\n".format(v.phone, v.phone2)
            if v.group and v.boss:
                s += "  {} ({})\n".format(v.group, v.boss)
            if v.office:
                s += "  {}\n".format(v.office)
            s += "  {}\n".format(v.id)

            for k in ["today", "tomorrow"]:

                day = getattr(v, k)

                if day:

                    if day.smart_working:
                        s += "  {} SMART_WORKING\n".format(k.upper())

                    if day.mission:
                        s += "  {} MISSION\n".format(k.upper())

                    if day.other:
                        s += "  {} OTHER\n".format(k.upper())

            if i != len(self.workers) - 1:
                s += "\n"

        return s
        return "\n".join(
            ["{} {}".format(v.name, v.status) for k, v in self.workers.items()]
        )

    def phone(self, phones):
        for p in phones:
            for k, v in self.address_phone.items():
                if p in v.phone or p in v.phone2:
                    self.workers[k] = v
        print(self)


def add_parser_address(parser):

    parser_group = parser.add_argument_group("worker options")

    parser_group.add_argument(
        "--in", dest="workers", metavar="worker", nargs="+", help="Worker's presence",
    )

    parser_group.add_argument(
        "-p",
        "--phone",
        dest="phones",
        metavar="phone",
        nargs="+",
        help="Worker's phone number",
    )

    parser_group.add_argument(
        "--cache-address", action="store_true", help="save address phone for future use"
    )


def main():

    parser = argparse.ArgumentParser(
        prog="PRaddress",
        description="presenzialo address",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser_address(parser)
    add_parser_debug(parser)

    args = parser.parse_args()

    pr_web = PRweb(PRauth(**vars(args)))

    if args.workers:
        pr_ins = PRaddress(pr_web, args.cache_address, args.raw)
        ins = pr_ins.present(args.workers)


if __name__ == "__main__":
    main()
