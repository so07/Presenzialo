import json
import datetime


def convert2time(minutes):
    t = datetime.datetime(1, 1, 1, 0, 0) + datetime.timedelta(minutes=minutes)
    return t.time()


def convert2date(s):
    year = int(s[0:4])
    month = int(s[4:6])
    day = int(s[6:8])
    return datetime.datetime(year, month, day)


def write_data(data, file):
    with open(file, "w") as fp:
        json.dump(data, fp, sort_keys=True, indent=4)


def read_data(file):
    with open(file, "r") as fp:
        data = json.load(fp)
    return data
