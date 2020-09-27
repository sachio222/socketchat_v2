from __future__ import print_function
import sys
import readline
from time import sleep
"""
https://stackoverflow.com/questions/37498704/print-text-before-input-prompt-in-python/37501797#37501797
"""
''' Print text in a scrolling region of the terminal above a fixed line for input

    Written by PM 2Ring 2016.05.29

    Python 2 / 3 version
'''

if sys.version_info > (3,):
    # Get the (current) number of lines in the terminal
    import shutil
    height = shutil.get_terminal_size().lines - 0

    stdout_write_bytes = sys.stdout.write
else:
    height = 40
    input = raw_input
    stdout_write_bytes = sys.stdout.write

# Some ANSI/VT100 Terminal Control Escape Sequences
# CSI = '\x1b['
CSI = '\033['
CLEAR = CSI + '2J'
CLEAR_LINE = CSI + '2K'
SAVE_CURSOR = CSI + 's'
UNSAVE_CURSOR = CSI + 'r'
DOWN_ONE = CSI + 'B'
HOME = CSI + '0;0H'
SCROLL = CSI + 'r'
SCROLL_UP = 'M'
SCROLL_DOWN = 'D'

GOTO_INPUT = CSI + '%d;0H' % (height)


def emit(*args):
    stdout_write_bytes(''.join(args))


emit(CLEAR, SAVE_CURSOR)
while True:
    buffer = input(">> ")

    print("user: ", buffer, end='\n')
