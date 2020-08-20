# print('\x1b[6;30;43m' + 'Success!' + '\x1b[0m')
for i in range(8):
    for j in range(20, 60):
        for k in range(32, 50):
            print(f'\x1b[{i};{j};{k}m' + f' {i};{j};{k} ' + '\x1b[0m', end='')

GREEN_UNDERLINE = '\x1b[4;32;38m'
RED = '\x1b[6;31;38m'
END = '\x1b[0m'

# Style, positon 1.
REG = 0
BOLD = 1
DIM = 2
ITALIC = 3
ULINE = 4
BLINK = 5
INVERT = 7

#BG, pos2.
BLACKB = 40
REDB = 41
GREENB = 42
GOLDB = 43
BLUEB = 44
PINKB = 45
CYANB = 46
GREYB = 47
NONEB = 48

# Text color, pos3
BLACKT = 30
REDT = 31
GREENT = 32
YELLOWT = 33
PURPLET = 34
PINKT = 35
CYANT = 36
GREYT = 37
WHITE = 38

FORMAT = f'\x1b[{REG};{BLUEB};{REDT}m'

print(F'{GREEN_UNDERLINE}WELCOME TO THE UNDERGROUND{END}')
print(f'{FORMAT} Testing some text {END}')
