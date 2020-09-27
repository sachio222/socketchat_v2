import socket
from chatutils import utils
from handlers.routers import ServerCmds
from lib.cmd import cmd

configs = utils.ConfigJSON()
HEADER_LEN = configs.system["headerLen"]

def _M_handler(sock: socket, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE HANDLER"""
    msg_len = sock.recv(HEADER_LEN)
    msg = sock.recv(int(msg_len))
    msg = msg.rstrip()
    print(msg.decode())
    return msg

def _X_handler(sock: socket, *args, **kwargs) -> bytes:
    """TRANSFER HANDLER"""
    pass

def _P_handler(sock: socket, *args, **kwargs):
    """ADD PUBLIC KEY"""
    pass

def _C_handler(sock: socket, *args, **kwargs):
    """COMMAND LINE CONTROL"""
    cmd.run_cmd(sock)


def error(*args, **kwargs):
    print(f'Message Type Error: Invalid message type {kwargs["msg_type"]}')
