import os

config_path = os.path.join(os.path.expanduser("~"), ".Presenzialo")

if not os.path.exists(config_path):
    os.makedirs(config_path)

config_auth = os.path.join(config_path, "auth")
config_pres = os.path.join(config_path, "presences")
