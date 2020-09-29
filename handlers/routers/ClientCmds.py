import socket
from chatutils import utils

configs = utils.JSONLoader()

BUFFER_LEN = configs.system["defaultBufferLen"]


def _M_handler(sock: socket, *args, **kwargs):
    response = b""
    recv_len = 1

    while recv_len:
        data = sock.recv(BUFFER_LEN)
        recv_len = len(data)
        response += data

        if recv_len < BUFFER_LEN:
            break

        if not data:
            break

    print(response.decode())


def error(sock: socket, *args, **kwargs):
    print("Whoops. You did wrong, Sucka!")


dispatch = {
    "a": None,
    "b": None,
    "c": None,
    "d": None,
    "e": None,
    "f": None,
    "g": None,
    "h": None,
    "i": None,
    "j": None,
    "k": None,
    "l": None,
    "m": None,
    "n": None,
    "o": None,
    "p": None,
    "q": None,
    "r": None,
    "s": None,
    "t": None,
    "u": None,
    "v": None,
    "w": None,
    "x": None,
    "y": None,
    "z": None,
    "A": None,
    "B": None,
    "C": None,
    "D": None,
    "E": None,
    "F": None,
    "G": None,
    "H": _M_handler,
    "I": None,
    "J": None,
    "K": None,
    "L": None,
    "M": _M_handler,
    "N": None,
    "O": None,
    "P": None,
    "Q": None,
    "R": None,
    "S": None,
    "T": None,
    "U": None,
    "V": None,
    "W": None,
    "X": None,
    "Y": None,
    "Z": None,
    "/": None
}
