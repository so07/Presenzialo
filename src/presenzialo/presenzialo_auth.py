#!/usr/bin/env python3
import os
import requests
import getpass
import base64

from configparser import ConfigParser

from .presenzialo_config import config_auth

PRauth_default = {
    "config_file": config_auth,
    "password_encoding": "base64",
    "remove_config_file": False,
    "save": False,
    "required": ["host", "username", "idpurl"],
}


class PRauth(dict):

    PRauth_config_option = "PRauth"

    def __init__(self, **kwargs):

        dict.__init__(self, **PRauth_default)
        # update with arguments
        self.update(kwargs)

        if self["remove_config_file"]:
            self._remove_config_file()

        # read from config_file
        self.update(self._read_config_file(self["config_file"]))
        # read from args
        self.update({k: kwargs[k] for k in self["required"] if kwargs.get(k, None)})

        self._check_required()

        if not self.get("password", False):
            self["password"] = self._encode(getpass.getpass())

        if self["save"]:
            self._write_config_file(self["config_file"])

    def _encode(self, _pass):

        if self["password_encoding"] == "base64":
            if isinstance(_pass, bytes):
                _pass = base64.b64encode(_pass)
            else:
                _pass = base64.b64encode(_pass.encode("ascii"))
        else:
            pass

        if isinstance(_pass, bytes):
            _pass = _pass.decode()

        return _pass

    def _decode(self, _pass):

        if self["password_encoding"] == "base64":
            _pass = base64.b64decode(_pass)
        else:
            pass

        return _pass

    def _check_required(self):
        missing = []
        for k in self["required"]:
            if not self.get(k, False):
                missing.append(k)
        if missing:
            raise Exception(
                "[PRauth] *** ERROR *** missing required args: {}".format(
                    ", ".join(missing)
                )
            )

    def _read_config_file(self, fname):
        """Read from config file"""

        if not os.path.isfile(fname):
            return {}

        parser = ConfigParser()
        parser.read(fname)

        return {
            k: parser.get(self.PRauth_config_option, k)
            for k in parser.options(self.PRauth_config_option)
        }

    def _write_config_file(self, fname):
        parser = ConfigParser()

        parser.add_section(self.PRauth_config_option)

        if self.get("host", None):
            parser.set(self.PRauth_config_option, "host", self["host"])
        if self.get("username", None):
            parser.set(self.PRauth_config_option, "username", self["username"])
        if self.get("idpurl", None):
            parser.set(self.PRauth_config_option, "idpurl", self["idpurl"])
        # if self.get('idemploy', None):
        #   parser.set(self.PRauth_config_option, 'idemploy', str(self['idemploy']))

        if self["save_password"]:
            parser.set(self.PRauth_config_option, "password", self["password"])

        with open(fname, "w") as f:
            parser.write(f)

    def _remove_config_file(self):
        if os.path.isfile(self["config_file"]):
            print("Removing config file :", self["config_file"])
            os.remove(self["config_file"])


def add_parser_auth(parser):

    authparser = parser.add_argument_group("authentication options")

    authparser.add_argument("-u", "--username", help="Username")

    # authparser.add_argument('-i', '--idemploy',
    #                        help='ID employee')

    authparser.add_argument("--url", dest="host", help="presence url")

    authparser.add_argument(
        "--idp", "--idp-url", dest="idpurl", help="Identity provider url"
    )

    authparser.add_argument(
        "-c",
        "--config-file",
        default=PRauth_default["config_file"],
        help="Configuration file (default %(default)s)",
    )

    authparser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Save PR authentication options in PRauth config file",
    )

    authparser.add_argument(
        "--save-password",
        action="store_true",
        help="Save PR authentication password in PRauth config file",
    )

    authparser.add_argument(
        "--remove-config-file", action="store_true", help="Remove PR config file"
    )

    args = parser.parse_args()

    return vars(args)


def main():

    import argparse

    parser = argparse.ArgumentParser(
        prog="presenzialo_authentication",
        description="Module to authenticate",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_parser_auth(parser)

    args = parser.parse_args()

    auth = PRauth(**vars(args))


if __name__ == "__main__":
    main()
