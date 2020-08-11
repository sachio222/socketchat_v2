#!/usr/bin/ python3

import sys


class Channel():
    """Returns room details"""

    def __init__(self):
        pass

    def get_status(self, addresses):
        """Returns people in the room when called, and outputs to channel"""
        people = []

        for user in addresses.keys():
            person = user
            people.append(f'@{person}')

        ppl_qty = len(people)
        ppl_lst = ', '.join(people)

        # Outputs
        # @YO: 4 online - @Jake, @toof, @veronica, @pizzanator
        room_status = f'{ppl_qty} online - {ppl_lst}'

        return room_status, people  # String


class Chime:
    # Ring my bell, ring my bell
    def __init__(self, muted=False):
        self.muted = muted

    def play_chime(self):
        if not self.muted:
            sys.stdout.write("\a")
            sys.stdout.flush()
        else:
            return

class Colors:
    def __init__(self):
        self.style = self.set_style()
        self.bg = self.set_bg()
        self.txt = self.set_txt()

    def set_style(self):
        # Text styles, positon 1
        style = {
            'REG' : 0,
            'BOLD' : 1,
            'DIM' : 2,
            'ITALIC' : 3,
            'ULINE' : 4,
            'BLINK' : 5,
            'INVERT' : 7
        }        
        return style
    
    def set_bg(self):
        # Background colors, position 2.
        bg = {
            'BLACK' :40,
            'RED':41,
            'GREEN':42,
            'GOLD':43,
            'BLUE':44,
            'PINK':45,
            'CYAN':46,
            'GREY':47,
            'NONE':48
        }
        return bg

    def set_txt(self):
        # Text color, pos3
        t = { 'BLACK':30,
            'RED':31,
            'GREEN':32,
            "GOLD":33,
            'BLUE':34,
            'PINK':35,
            'CYAN':36,
            'GREY':37,
            'WHITE':38}
        return t

    def format(self, styl, bg, txt):
        s = self.style.get(styl)
        bg = self.bg.get(bg)
        t = self.txt.get(txt)
        return f'\x1b[{s};{bg};{t}m'
    
    def make_fancy(self, fmt, msg):
        # Returns formatted string.
        END = '\x1b[0m'
        msg = f'{fmt}{msg}{END}'
        return msg
