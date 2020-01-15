import os
import datetime

config_path = os.path.join(os.path.expanduser("~"), ".Presenzialo")

if not os.path.exists(config_path):
    os.makedirs(config_path)

config_auth = os.path.join(config_path, "auth")
config_presences = os.path.join(config_path, "presences")
config_address = os.path.join(config_path, "address")
config_workersid = os.path.join(config_path, "workersid")

config_workersid_deadline = datetime.timedelta(days=7)
config_address_deadline = datetime.timedelta(days=31)


def check_file_date(config_file):
    return datetime.datetime.fromtimestamp(os.path.getmtime(config_file))


def generate_workersid_file():

    try:
        time = check_file_date(config_workersid)
    except FileNotFoundError:
        return True

    dt = datetime.datetime.now() - time

    return dt > config_workersid_deadline
