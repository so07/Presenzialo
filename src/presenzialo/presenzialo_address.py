import argparse
import json

from .presenzialo_web import PRweb
from .presenzialo_auth import PRauth
from .presenzialo_config import generate_workersid_file, config_workersid
from .presenzialo_id import PRworker

from collections import namedtuple, OrderedDict

Worker = namedtuple("Worker", "name id status phone phone2")


class PRaddress:
    def __init__(self, pr_web, raw=False):

        self.pr_web = pr_web
        self.pr_ids = PRworker(pr_web)

        self.workers = OrderedDict()

        self.raw = raw

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
            w = Worker(
                i["nominativo"], i["id"], i["descrstato"], i["telefono"], i["libero"]
            )
            d[w.id] = w
        return d

    def __str__(self):
        s = ""
        for i, (k, v) in enumerate(self.workers.items()):
            s += "{}\n{}\n".format(v.name, v.status)
            s += "{} {}\n".format(v.phone, v.phone2)
            s += "{}\n".format(v.id)
            if i != len(self.workers) - 1:
                s += "\n"
        return s
        return "\n".join(
            ["{} {}".format(v.name, v.status) for k, v in self.workers.items()]
        )


def add_parser(parser):

    parser_group = parser.add_argument_group("Worker options")

    parser_group.add_argument(
        "--in",
        dest="workers_for_in",
        metavar="worker",
        nargs="+",
        help="Worker's presence",
    )

    parser_group.add_argument("--raw", action="store_true", help="raw data")


def main():

    parser = argparse.ArgumentParser(
        prog="PRaddress",
        description="presenzialo address",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser(parser)

    args = parser.parse_args()

    pr_web = PRweb(PRauth(**vars(args)))

    if args.workers_for_in:
        pr_ins = PRaddress(pr_web, args.raw)
        ins = pr_ins.present(args.workers_for_in)


if __name__ == "__main__":
    main()
