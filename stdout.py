# # myName = input()
# # print("\x1B[F\x1B[2K", end="")
# # print("My name is: " + myName)

# import sys

# myName = input()

# sys.stdout.write("\033[F") # Cursor up one line

# print("My name is: " + myName)

# import curses

# def main(win):
#     win.addstr(win.getmaxyx()[0] - 1, 0, 'Hello World!')
#     win.refresh()
#     win.getch()

# curses.wrapper(main)

''' Print text in a scrolling region of the terminal above a fixed line for input

    Written by PM 2Ring 2016.05.29

    Python 2 / 3 version
'''

from __future__ import print_function
import sys
import readline

if sys.version_info > (3,):
    # Get the (current) number of lines in the terminal
    import shutil
    height = shutil.get_terminal_size().lines - 1

    stdout_write_bytes = sys.stdout.buffer.write
else:
    height = 40
    input = raw_input
    stdout_write_bytes = sys.stdout.write


# Some ANSI/VT100 Terminal Control Escape Sequences
CSI = b'\x1b['
CLEAR = CSI + b'2J'
CLEAR_LINE = CSI + b'2K'
SAVE_CURSOR = CSI + b's'
UNSAVE_CURSOR = CSI + b'u'

GOTO_INPUT = CSI + b'%d;0H' % (height + 1)

def emit(*args):
    stdout_write_bytes(b''.join(args))

def set_scroll(n):
    return CSI + b'0;%dr' % n

emit(CLEAR, set_scroll(height))

try:
    while True:
        #Get input
        emit(SAVE_CURSOR, GOTO_INPUT, CLEAR_LINE)
        try:
            n = input('>> ')
        except ValueError:
            continue
        finally:
            emit(UNSAVE_CURSOR)

        #Display some output
        print(f'@username: {n}')

except KeyboardInterrupt:
    #Disable scrolling, but leave cursor below the input row
    emit(set_scroll(0), GOTO_INPUT, b'\n')

