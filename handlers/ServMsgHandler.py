import socket
from chatutils import utils
from handlers.routers import ServerCmds

configs = utils.ConfigJSON()

HEADER_LEN = configs.system["headerLen"]

def dispatch(sock: socket, msg_type: str):
    """Sorts through incoming data by prefix."""
    assert type(msg_type) == bytes, "Convert prefix to str"
    func = dispatch_cmds.get(msg_type.decode(), error)
    func(sock=sock, msg_type=msg_type)

def _M_handler(sock: socket, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE HANDLER"""
    msg_len = sock.recv(HEADER_LEN)
    msg = sock.recv(int(msg_len))
    msg = msg.rstrip()
    print(msg.decode())
    return msg

def error(*args, **kwargs):
    print(f'Message Type Error: Invalid message type {kwargs["msg_type"]}')

dispatch_cmds = {
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
    "H": None,
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