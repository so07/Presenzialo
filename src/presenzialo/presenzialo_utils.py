import datetime


def convert2time(minutes):
    t = datetime.datetime(1, 1, 1, 0, 0) + datetime.timedelta(minutes=minutes)
    return t.time()


def convert2date(s):
    year = int(s[0:4])
    month = int(s[4:6])
    day = int(s[6:8])
    return datetime.datetime(year, month, day)
