import os
import sys
import socket

from chatutils import utils
configs = utils.JSONLoader()

BUFFER_LEN = configs.dict["system"]["bufferLen"]

def write(sock):
    path = 'testfile1.jpg'

    while True:
        file_buffer = b""
        recv_len = 1

        try:
            while recv_len:
                data = sock.recv(BUFFER_LEN)
                recv_len = len(data)

                # Overwrite file if exists.
                with open(path, 'wb') as f:
                    f.write(data)

                if recv_len < BUFFER_LEN:
                    break

                else:
                    with open(path, 'ab') as f:
                        while True:
                            data = sock.recv(BUFFER_LEN)
                            recv_len = len(data)

                            # Append rest of data chunks
                            f.write(data)

                            if recv_len < BUFFER_LEN:
                                break
                break

            if not data:
                break

            sock.send(b"M")
            sock.send(b"Successfully saved file.")
            sock

        except:
            sock.send(b"M")
            sock.send(b"File transfer failed.")


def write_file(sock: socket,
               path: str = "testimage1.jpg",
               recv_len: int = 1,
               open_mode: str = "wb"):

    if recv_len:
        data = sock.recv(BUFFER_LEN)
        recv_len = len(data)

        with open(path, open_mode) as f:
            f.write(data)

        if recv_len < BUFFER_LEN:
            sock.send(b"File successfully transfered.")
            return
        else:
            write_file(path, sock, recv_len, "ab")
