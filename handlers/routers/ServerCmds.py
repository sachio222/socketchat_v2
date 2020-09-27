import socket
from chatutils import utils
from chatutils.chatio2 import ChatIO
from handlers.routers import ServerCmds
from lib.cmd import cmd

configs = utils.JSONLoader()
HEADER_LEN = configs.system["headerLen"]


def _M_handler(sock: socket, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE HANDLER"""
    msg_bytes = ChatIO.unpack_data(sock)
    print(msg_bytes.decode())
    # ChatIO.broadcast(sock, user_dict)
    return msg_bytes


def _X_handler(sock: socket, *args, **kwargs) -> bytes:
    """TRANSFER HANDLER"""
    pass


def _P_handler(sock: socket, *args, **kwargs):
    """ADD PUBLIC KEY"""
    pass


def _C_handler(sock: socket, *args, **kwargs):
    """COMMAND LINE CONTROL"""
    print("cli running")
    cmd.commands(sock)


def error(*args, **kwargs):
    print(f'Message Type Error: Invalid message type {kwargs["msg_type"]}')
