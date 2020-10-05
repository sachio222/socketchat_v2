import json, socket
from sys import prefix
from chatutils import utils
from chatutils.chatio2 import ChatIO

from lib.xfer import download

from handlers import HandshakeHandler
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
    data_dict = json.loads(bytes_data)
    ChatIO.print_to_client(ChatIO, data_dict)

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
    "f": _f_handler,
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
    "r": _r_handler,
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
