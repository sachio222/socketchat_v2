import os
import sys
from sys import hash_info
import time
import json
import socket

import argon2
import config.filepaths as paths


def get_file_size(path: str):
    os.path.getsize(path)


def countdown(secs=90, msg='-+- Try again in '):
    # util
    ERASE_LINE = '\x1b[2K'
    t = secs
    while t >= 0:
        print(f'{msg}{t}\r', end="")
        sys.stdout.write(ERASE_LINE)
        time.sleep(1)
        t -= 1
    exit()


def print_from_file(path):
    # Opens path and prints contents.
    ok_ext = set(['txt'])  # Accepted file ext.
    _, ext = split_path_ext(path)
    assert ext in ok_ext, f"{ext} is not a valid Extension. Use a valid file."

    with open(path, 'rb') as f:
        msg = f.read().decode()
        print(msg)


def split_path_ext(path):
    # Splits file extension.
    parts = path.split('.')  # Splits at period

    # TODO: Add support for more than one period.
    main = parts[:-1][0]  # main part
    ext = parts[-1]  # extension.

    return main, ext


class JSONLoader():
    """Loads and updates config.json file listed in config/filepaths.py"""

    def __init__(self, path=paths.json_path):
        self.load(path)

    def load(self, path=paths.json_path):
        with open(path) as f:
            configs = json.load(f)
            self.__dict__.update(configs)

    def update(self, path=paths.json_path):
        with open(path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    reload = load

    @property
    def dict(self):
        """Access class as dict."""
        self.__dict__


def store_user(sock: socket,
               addr: tuple,
               new_user: dict,
               nick: str = None,
               public_key: bytes = None,
               trusted: list = None) -> dict:
    """SERVERSIDE USER DICT"""
    try:
        users = JSONLoader(paths.user_dict_path)
    except Exception as e:
        print(f"ERROR: Problem with JSON file at {paths.user_dict_path}. "\
              "Check for hanging comma or brackets and stuff.")
        exit()

    new_user_dict = json.loads(new_user)

    # Fill structure with overrides or defaults.
    new_user_dict = {
        "nick": new_user_dict.get("nick", None) or nick,
        "addr": new_user_dict.get("addr", None) or addr,
        "public_key": new_user_dict.get("public_key", None) or public_key,
        "trusted": new_user_dict.get("trusted", None) or trusted
    }

    users.__dict__[new_user_dict["nick"]] = new_user_dict
    users.update(paths.user_dict_path)

    return users.__dict__


def delete_user(nick: str):
    user_dict = JSONLoader(paths.user_dict_path)
    del user_dict.__dict__[nick]
    user_dict.update(paths.user_dict_path)
