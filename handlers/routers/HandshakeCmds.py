import socket
from chatutils import utils
from chatutils.chatio2 import ChatIO

from handlers import HandshakeHandler

import config.filepaths as paths
prefixes = utils.JSONLoader(paths.prefix_path)


def _n_handler(sock: socket, *args, **kwargs):
    """REQUEST NICK"""
    bytes_data = ChatIO.unpack_data(sock).decode()
    nick = HandshakeHandler.ClientSide.show_nick_request(sock,
                                                         prompt=bytes_data)
    ChatIO().pack_n_send(sock, prefixes.dict["client"]["handshake"]["nick"],
                         nick.encode())
    return nick


def _u_handler(sock: socket, *args, **kwargs):
    """User was Unique"""
    data = ChatIO.unpack_data(sock)
    return data


def _N_handler(sock: socket, *args, **kwargs):
    pass


def error(*args, **kwarfs):
    print("nope nope")


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
    "n": _n_handler,
    "o": None,
    "p": None,
    "q": None,
    "r": None,
    "s": None,
    "t": None,
    "u": _u_handler,
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
    "H": None,
    "I": None,
    "J": None,
    "K": None,
    "L": None,
    "M": None,
    "N": _N_handler,
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
