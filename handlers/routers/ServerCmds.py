import socket
from chatutils import utils
from chatutils.chatio2 import ChatIO
from handlers import HandshakeHandler
from lib.cmd import cmd

configs = utils.JSONLoader()
HEADER_LEN = configs.dict["system"]["headerLen"]


def _i_handler(sock: socket, *args, **kwargs):
    print("pinged back")

def _n_handler(sock: socket, *args, **kwargs) -> bytes:
    "RETURNS NICK FROM CLIENT"
    msg_bytes = ChatIO.unpack_data(sock)
    return msg_bytes


def _C_handler(sock: socket, *args, **kwargs):
    """COMMAND LINE CONTROL"""
    cmd.commands(sock)


def _D_handler(sock: socket, *args, **kwargs) -> bytes:
    """DATA FROM CLIENT"""
    bytes_data = ChatIO.unpack_data(sock)
    return bytes_data


def _H_handler(sock: socket, *args, **kwargs) -> bytes:
    """RECEIVE HANDSHAKE DICT"""
    bytes_data = ChatIO.unpack_data(sock)
    return bytes_data


def _M_handler(sock: socket, buffer: dict, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE HANDLER"""
    msg_bytes = buffer["msg_bytes"] = ChatIO.unpack_data(sock)
    ChatIO().broadcast(sock, buffer)
    return msg_bytes


def _X_handler(sock: socket, *args, **kwargs) -> bytes:
    """TRANSFER HANDLER"""
    pass


def _P_handler(sock: socket, *args, **kwargs):
    """ADD PUBLIC KEY"""
    pass


def error(*args, **kwargs):
    print(f'Message Type Error: Invalid message type {kwargs["msg_type"]}')


dispatch = {
    "a": None,
    "b": None,
    "c": None,
    "d": None,
    "e": None,
    "f": None,
    "g": None,
    "h": None,
    "i": _i_handler,
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
    "C": _C_handler,
    "D": _D_handler,
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
    "W": None,
    "X": None,
    "Y": None,
    "Z": None,
    "/": None
}
