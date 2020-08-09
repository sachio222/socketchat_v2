import os
import sys
import time


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
