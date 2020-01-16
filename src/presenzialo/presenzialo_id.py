import json
import argparse

from .presenzialo_web import PRweb
from .presenzialo_auth import PRauth
from .presenzialo_config import generate_workersid_file, config_workersid
from .presenzialo_args import add_parser_debug
from .presenzialo_utils import write_data, read_data

from collections import namedtuple, OrderedDict

WorkerID = namedtuple("WorkerID", "surname name total id")


class PRworker:
    def __init__(self, pr_web, raw=False):

        self.pr_web = pr_web
        self.raw = raw

        if generate_workersid_file():
            data = self.download()
            write_data(data, config_workersid)
        else:
            data = read_data(config_workersid)

        self.workers, self.num_workers = self.parse(data)

    def download(self):
        return self.pr_web.workers_id()

    def parse(self, json):
        d = OrderedDict()
        for i in json["results"]:
            if self.raw:
                print(i)
            d[i["iddip"]] = WorkerID(
                i["cognome"],
                i["nome"],
                "{} {}".format(i["nome"], i["cognome"]),
                i["iddip"],
            )
        return d, json["total"]

    def __str__(self):
        return "\n".join(
            "{:5d} {} {}".format(v.id, v.surname, v.name)
            for k, v in self.workers.items()
        )

    def id(self, name):
        if isinstance(name, str):
            name = [name]
        # upper case
        name = [n.upper() for n in name]
        l = []
        for n in name:
            for k, v in self.workers.items():
                if n in v.total:
                    l.append(v.id)
        return l

    def worker(self, id):
        w = self.workers[id]
        return "{} {}".format(w.surname, w.name)

    def total(self):
        return self.num_workers


def add_parser(parser):

    parser_group = parser.add_argument_group("worker options")

    parser_group.add_argument(
        "--id",
        dest="workers_for_id",
        metavar="worker",
        nargs="+",
        default=None,
        help="Worker's id",
    )


def main():

    parser = argparse.ArgumentParser(
        prog="PRids",
        description="presenzialo address",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser(parser)
    add_parser_debug(parser)

    args = parser.parse_args()

    pr_web = PRweb(PRauth(**vars(args)))

    if args.workers_for_id:
        pr_ids = PRworker(pr_web, args.raw)
        ids = pr_ids.id(args.workers_for_id)
        print("\n".join(["{} {}".format(i, pr_ids.worker(i)) for i in ids]))


if __name__ == "__main__":
    main()
