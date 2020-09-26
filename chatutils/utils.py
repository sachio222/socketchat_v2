import os
import sys
import time
import json

# from pathlib2 import Path
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


class ConfigJSON():
    """Loads and updates config.json file listed in config/filepaths.py"""

    def __init__(self):
        self.load(paths.json_path)

    def load(self, path=paths.json_path):
        with open(path) as f:
            configs = json.load(f)
            self.__dict__.update(configs)

    def update(self, path=paths.json_path):
        with open(path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    @property
    def dict(self):
        """Access class as dict."""
        self.__dict__

