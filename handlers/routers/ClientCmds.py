import json
import socket
from chatutils import utils
from chatutils.chatio2 import ChatIO

from handlers import HandshakeHandler

configs = utils.JSONLoader()

BUFFER_LEN = configs.dict["system"]["defaultBufferLen"]


def _n_handler(sock: socket, *args, **kwargs):
    # print("running nhandler")
    bytes_data = ChatIO.unpack_data(sock)
    return bytes_data


def _H_handler(sock: socket, *args, **kwargs):
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data)
    return bytes_data


def _W_handler(sock: socket, *args, **kwargs):
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data.decode())
    return bytes_data


def _M_handler(sock: socket, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE"""
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data.decode())

    return bytes_data
    # response = b""
    # recv_len = 1

    # while recv_len:
    #     data = sock.recv(BUFFER_LEN)
    #     recv_len = len(data)
    #     response += data

    #     if recv_len < BUFFER_LEN:
    #         break

    #     if not data:
    #         break
    # print(response.decode())


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
    "n": _n_handler,
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
    "H": _H_handler,
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
    "W": _W_handler,
    "X": None,
    "Y": None,
    "Z": None,
    "/": None
}
