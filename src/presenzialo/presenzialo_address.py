import argparse
import json

from .presenzialo_web import PRweb
from .presenzialo_auth import PRauth
from .presenzialo_config import generate_workersid_file, config_workersid

from collections import namedtuple, OrderedDict

WorkerID = namedtuple("WorkerID", "surname name total id")
Worker = namedtuple("Worker", "name id status phone phone2")


class PRaddress:
    def __init__(self, pr_web):

        self.pr_web = pr_web
        self.pr_ids = PRworker(pr_web)

        self.workers = OrderedDict()

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


class PRworker:
    def __init__(self, pr_web):

        self.pr_web = pr_web

        if generate_workersid_file():
            data = self.download()
            self.write(data)
        else:
            data = self.read()

        self.workers, self.num_workers = self.parse(data)

    def download(self):
        return self.pr_web.workers_id()

    def write(self, js):
        with open(config_workersid, "w") as fp:
            json.dump(js, fp, sort_keys=True, indent=4)

    def read(self):
        with open(config_workersid, "r") as fp:
            data = json.load(fp)
        return data

    def parse(self, json):
        d = OrderedDict()
        for i in json["results"]:
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

    parser_group = parser.add_argument_group("Worker options")

    parser_group.add_argument(
        "--id",
        dest="worker_for_id",
        metavar="worker",
        default=None,
        help="Worker's id",
    )

    parser_group.add_argument(
        "--in",
        dest="workers_for_in",
        metavar="worker",
        default=None,
        help="Worker's presence",
    )


def main():

    parser = argparse.ArgumentParser(
        prog="PRaddress",
        description="presenzialo address",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser(parser)

    args = parser.parse_args()

    pr_web = PRweb(PRauth(**vars(args)))

    if args.worker_for_id:
        pr_ids = PRworker(pr_web)
        ids = pr_ids.id(args.worker_for_id)
        print("\n".join(["{} {}".format(i, pr_ids.worker(i)) for i in ids]))

    if args.workers_for_in:
        pr_ins = PRaddress(pr_web)
        ins = pr_ins.present(args.workers_for_in)

        # ids = pr_ids.id(args.workers_for_in)
        # print("\n".join(["{} {}".format(i, pr_ids.worker(i)) for i in ids]))


if __name__ == "__main__":
    main()
