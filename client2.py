#!/usr/bin/ python3
"""Encryptochat 2.0"""
from enum import unique
from handlers import ClientMsgHandler
import sys
import socket
from threading import Thread
import config.filepaths as paths
from chatutils import utils
from chatutils.chatio2 import ChatIO

from handlers import HandshakeHandler, InputHandler

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)

PREFIX_LEN = configs.system["prefixLen"]
BUFFER_LEN = configs.system["defaultBufferLen"]
HEADER_LEN = configs.system["headerLen"]
TARGET_HOST = configs.system["defaultHost"]
TARGET_PORT = configs.system["defaultPort"]

USER_ID = ""


class Client(ChatIO):

    def __init__(self):
        configs.session["isUniqueId"] = False
        configs.update()

    def connect(self):
        global USER_ID

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TARGET_HOST, TARGET_PORT))

            configs = utils.JSONLoader()
            print(configs.session["isUniqueId"])
            USER_ID = HandshakeHandler.ClientHand(sock).nick
            
            self.start_threads(sock)

        except Exception as e:
            print(e)
            print("[x] Connection failed. Check server address or port.")
            sock.close()

    def send(self, sock):
        while True:
            buffer = input("")
            print("\x1B[F\x1B[2K", end="")
            print(f"@{USER_ID}: " + buffer)

            output_bytes = InputHandler.dispatch(sock, buffer)
            # print(output_bytes)

            if output_bytes:
                self.pack_n_send(sock, prefixes.client["msg"], output_bytes)

            # if buffer == "upload":
            #     self.upload(sock)
            # else:
            #     buffer += "\n"
            #     buffer = self.pack_n_send(sock, "M", buffer)

    def upload(self, sock):
        path = "image.jpg"
        with open(path, 'rb') as f:
            f = self.pack_data("D", f)
            print(f)
            # sock.sendfile(f)

    def listen(self, sock):
        while True:
            # try:
            msg_type = sock.recv(PREFIX_LEN)

            if not msg_type:
                break

            ClientMsgHandler.dispatch(sock, msg_type)
            # except:
            #     response = b""
            #     recv_len = 1

            #     while recv_len:
            #         data = sock.recv(BUFFER_LEN)
            #         recv_len = len(data)
            #         response += data

            #         if recv_len < BUFFER_LEN:
            #             break

            #         if not data:
            #             break

                # print(response.decode())

        self.killit(sock)

    def start_threads(self, sock):
        listening_thread = Thread(target=self.listen, args=(sock,))
        listening_thread.start()

        # daemon=True terminates sending_thread when listening_thread is closed.
        sending_thread = Thread(target=self.send, args=(sock,), daemon=True)
        sending_thread.start()

    def killit(self, sock):
        sock.close()
        print("Server Disconnected.")
        sys.exit()


def main():
    client.connect()


if __name__ == "__main__":
    client = Client()
    main()
