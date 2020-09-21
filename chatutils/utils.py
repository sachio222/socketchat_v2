import os
import sys
import time
import json


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

class JSONConfig():

    def __init__(self, json_path):
        with open(json_path) as f:
            cfg_json = json.load(f)
            self.__dict__.update(cfg_json)

    def save(self, json_path):
        with open(json_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, json_path):
        """Loads parameters from json file."""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by 'params.dict['learning_rate]."""
        return self.__dict__