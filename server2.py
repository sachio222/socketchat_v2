import sys
import sqlite3
import subprocess
import socket
from threading import Thread
from handlers import ServMsgHandler

from chatutils import utils

# sys.setrecursionlimit(20000)
configs = utils.ConfigJSON()
BUFFER_LEN = configs.system["defaultBufferLen"]
HOST = configs.system["defaultHost"]
PORT = configs.system["defaultPort"]
ADDR = (HOST, PORT)


def accept_client(server):
    while True:
        client_socket, addr = server.accept()
        nick = client_socket.recv(22).decode()
        print("nick is", nick)
        user_dict = utils.store(client_socket, addr, nick=nick)
        print(f"Connected to {addr}")
        welcome_msg = f"Welcome to {ADDR}"
        client_socket.send(welcome_msg.encode())
        client_thread = Thread(target=handle_client,
                               args=(client_socket,),
                               daemon=True)
        client_thread.start()


def handle_client(client_socket):
    PREFIX_LEN = configs.system["prefixLength"]
    while True:
        msg_type = client_socket.recv(PREFIX_LEN)

        if not msg_type:
            break

        ServMsgHandler.dispatch(client_socket, msg_type)

    client_socket.close()


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


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    print(f"Server spinning up at {ADDR}")
    server.listen(5)
    print(f"Listening for connections...")

    accept_thread = Thread(target=accept_client, args=(server,))
    accept_thread.start()


if __name__ == "__main__":
    main()
