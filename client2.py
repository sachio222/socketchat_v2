#!/usr/bin/ python3
"""Encryptochat 2.0"""
import socket, ssl
from threading import Thread
from chatutils import utils, channel2
from chatutils.chatio2 import ChatIO
from handlers import HandshakeHandler, InputHandler, ClientMsgHandler
from lib.encryption import x509

import config.filepaths as paths
configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)

PREFIX_LEN = configs.dict["system"]["prefixLen"]
BUFFER_LEN = configs.dict["system"]["bufferLen"]
HEADER_LEN = configs.dict["system"]["headerLen"]
TARGET_HOST = configs.dict["system"]["defaultHost"]
TARGET_PORT = configs.dict["system"]["defaultPort"]

USER_ID = ""


class Client(ChatIO):

    def __init__(self):
        pass

    def connect(self):
        global USER_ID

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TARGET_HOST, TARGET_PORT))

            # ******** SSL WRAPPER ********#
            sock = client_ctxt.wrap_socket(sock, server_hostname=TARGET_HOST)
            print(f'[+] SSL Established. {sock.version()}')
            # ******** SSL WRAPPER ********#

            configs.reload()

            USER_ID = HandshakeHandler.ClientSide(sock).nick

            self.start_threads(sock)

        except Exception as e:
            print(e)
            print("[x] Connection failed. Check server address or port.")

    def send(self, sock):
        while True:
            buffer = input("")

            print("\x1B[F\x1B[2K", end="")
            print(f"@{USER_ID}: " + buffer)

            output_bytes, msg_type = InputHandler.dispatch(sock, buffer)

            if output_bytes:
                self.pack_n_send(sock, msg_type, output_bytes)

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

        Thread.join()
        channel2.killit(sock)

    def start_threads(self, sock):
        listening_thread = Thread(target=self.listen, args=(sock,))
        listening_thread.start()

        # daemon=True terminates sending_thread when listening_thread is closed.
        sending_thread = Thread(target=self.send, args=(sock,), daemon=True)
        sending_thread.start()


def main():
    client = Client()
    client.connect()


if __name__ == "__main__":

    # ******** SSL CONTEXT ********#
    x509.X509()
    rsa_key_path = paths.x509_path + 'rsa_key.pem'
    cert_path = paths.x509_path + 'certificate.pem'

    client_ctxt = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    client_ctxt.check_hostname = False
    client_ctxt.verify_mode = ssl.CERT_NONE
    client_ctxt.set_ciphers('ECDHE-ECDSA-AES256-SHA384')
    client_ctxt.options |= ssl.OP_NO_COMPRESSION
    client_ctxt.load_verify_locations(cert_path)
    # ******** SSL CONTEXT ********#

    main()
