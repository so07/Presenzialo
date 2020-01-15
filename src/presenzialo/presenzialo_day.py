from .logs.daylog import DayLog

from .presenzialo_utils import convert2time, convert2date
import datetime


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

            # print(k_orari)
            # print(type(timbrature), timbrature)
            timbs = [i[k_orari] for i in timbrature["data"]]
            timbs = [convert2time(i).strftime("%H:%M") for i in timbs]
            # print(d[k_data], [convert2time(i).strftime("%H:%M") for i in timbs])
            # convert2time(timbs[0])

            if len(timbs) % 2 != 0:
                timbs.append(datetime.datetime.now().strftime("%H:%M"))

            d = DayLog(convert2date(d[k_data]), timbs)

            self.days.append(d)
