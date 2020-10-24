import json, socket
from chatutils import utils
from chatutils.chatio2 import ChatIO

from lib.xfer import download
from lib.encryption import CipherTools
from handlers import DecryptionHandler, EncryptionHandler

import config.filepaths as paths

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)

BUFFER_LEN = configs.dict["system"]["bufferLen"]

def _f_handler(sock: socket, *args, **kwargs):
    """INCOMING FILE INFO"""
    pass

def _i_handler(sock: socket, *args, **kwargs):
    """IDLE PING LISTENER"""
    print("@Yo: Ping from server!")
    sock.send(b"i")

def _l_handler(sock: socket, *args, **kwargs):
    """LINE BREAK"""
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data.decode())


def _n_handler(sock: socket, *args, **kwargs):
    # print("running nhandler")
    bytes_data = ChatIO.unpack_data(sock)
    return bytes_data

def _r_handler(sock: socket, *args, **kwargs):
    """RECEIVE FILE AND WRITE TO DISK"""
    download.write(sock=sock)

    # incoming = b""
    # recv_len = 1

    # while recv_len:
    #     data = sock.recv(BUFFER_LEN)
    #     recv_len = len(data)
    #     incoming += data

    #     if recv_len < BUFFER_LEN:
    #         break

    #     if not data:
    #         break
    
    # with open("testfile.img", 'wb') as f:
    #     f.write(incoming)

def _s_handler(sock: socket, *args, **kwargs) -> bytes:
    """INCOMING SERVER MESSAGES."""
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data.decode())
    return bytes_data

def _u_handler(sock: socket, *args, **kwargs):
    """UPLOAD FILE TO SERVER"""
    data = prefixes.dict["upload"]
    
    # if file exists:
    if True:
        sock.send(data.encode())
        print("Sending file")
        with open("testfile.jpg", "rb") as f:
            sent_bytes = sock.sendall(f)
            print(sent_bytes)
    else:
        # File doesn't exist error. 
        pass

def _C_handler(sock: socket, *args, **kwargs):
    """INCOMING CMD LINE"""
    ChatIO.recv_open(sock)
    # sock.recv(1)
    # pass
        


def _H_handler(sock: socket, *args, **kwargs):
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data)
    return bytes_data


def _W_handler(sock: socket, *args, **kwargs):
    bytes_data = ChatIO.unpack_data(sock)
    print(bytes_data.decode())
    return bytes_data


def _M_handler(sock: socket, *args, **kwargs) -> bytes:
    """DEFAULT MESSAGE DICTS"""
    bytes_data = ChatIO.unpack_data(sock)
    try:
        data_dict = json.loads(bytes_data)
    except:
        data_dict = bytes_data
    sender, msg = DecryptionHandler.message_router(data_dict)
    ChatIO.print_to_client(ChatIO, sender, msg)

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

def _T_handler(sock: socket, *args, **kwargs) -> bytes:
    """RECEIVES PUBKEYS FROM SERVER"""
    pub_key_trustee = ChatIO().unpack_data(sock)
    print('What to do wth pub_key:',pub_key_trustee)
    CipherTools.make_nacl_pub_box(pub_key=pub_key_trustee)
    
    return pub_key_trustee


def error(sock: socket, *args, **kwargs):
    print("Whoops. You did wrong, Sucka!")


dispatch = {
    "a": None,
    "b": None,
    "c": None,
    "d": None,
    "e": None,
    "f": _f_handler,
    "g": None,
    "h": None,
    "i": _i_handler,
    "j": None,
    "k": None,
    "l": _M_handler,
    "m": None,
    "n": _n_handler,
    "o": None,
    "p": None,
    "q": None,
    "r": _r_handler,
    "s": _s_handler,
    "t": None,
    "u": _u_handler,
    "v": None,
    "w": None,
    "x": None,
    "y": None,
    "z": None,
    "A": None,
    "B": None,
    "C": _C_handler,
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
    "T": _T_handler,
    "U": None,
    "V": None,
    "W": _W_handler,
    "X": None,
    "Y": None,
    "Z": None,
    "/": None
}
