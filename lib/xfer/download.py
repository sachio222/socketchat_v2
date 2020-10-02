import os
from server2 import BUFFER_LEN
import sys
import socket

from chatutils import utils
configs = utils.JSONLoader()

BUFFER_LEN = configs.dict["system"]["defaultBufferLen"]


def download(client_socket):
    path = 'Tamarindo-Concepts2.pdf'

    while True:
        file_buffer = b""
        recv_len = 1

        try:
            while recv_len:
                data = client_socket.recv(BUFFER_LEN)
                recv_len = len(data)

                # Overwrite file if exists.
                with open(path, 'wb') as f:
                    f.write(data)

                if recv_len < BUFFER_LEN:
                    break

                else:
                    with open(path, 'ab') as f:
                        while True:
                            data = client_socket.recv(BUFFER_LEN)
                            recv_len = len(data)

                            # Append rest of data chunks
                            f.write(data)

                            if recv_len < BUFFER_LEN:
                                break
                break

            if not data:
                break

            client_socket.send(b"Successfully saved file.")

        except:
            client_socket.send(b"File transfer failed.")


def write_file(path: str,
               client_socket: socket,
               recv_len: int = 1,
               open_mode: str = "wb"):

    if recv_len:
        data = client_socket.recv(BUFFER_LEN)
        recv_len = len(data)

        with open(path, open_mode) as f:
            f.write(data)

        if recv_len < BUFFER_LEN:
            client_socket.send(b"File successfully transfered.")
            return
        else:
            write_file(path, client_socket, recv_len, "ab")
