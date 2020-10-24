import socket, ssl

from threading import Thread
from handlers import HandshakeHandler, ServMsgHandler
from lib.encryption import x509

from chatutils import utils
from chatutils.chatio2 import ChatIO

import config.filepaths as paths

configs = utils.JSONLoader()
users = utils.JSONLoader(paths.user_dict_path)
users.clear()

BUFFER_LEN = configs.dict["system"]["bufferLen"]
PREFIX_LEN = configs.dict["system"]["prefixLen"]

HOST = configs.dict["system"]["defaultHost"]
PORT = configs.dict["system"]["defaultPort"]
ADDR = (HOST, PORT)

sockets_dict = {}
active_sockets = []


def accept_client(server):

    while True:
        client_socket, addr = server.accept()

        # ******** SSL WRAPPER ******** #
        client_socket = server_ctxt.wrap_socket(client_socket, server_side=True)
        # ******** SSL WRAPPER ******** #

        active_sockets.append(client_socket)

        print(f"[+] Connected to {addr}")

        client_thread = Thread(target=handle_client,
                               args=(client_socket, addr),
                               daemon=True)

        client_thread.start()


def handle_client(client_socket: socket, addr: tuple) -> None:

    user_dict = HandshakeHandler.ServerSide(client_socket, addr).user
    print(f"[+] {user_dict['nick']} has joined the chat.")

    sockets_dict[user_dict["nick"]] = client_socket

    while True:
        msg_type = client_socket.recv(PREFIX_LEN)
        # utils.debug_(msg_type, "msg_type", "handle_cient", True)

        if not msg_type:
            del sockets_dict[user_dict["nick"]]
            utils.delete_user(user_dict["nick"])
            break

        buffer = ChatIO.make_buffer(sockets_dict, user_dict, msg_type)
        # utils.debug_(buffer, "buffer")

        ServMsgHandler.dispatch(client_socket, buffer)

    client_socket.close()


def das_boot():

    import time
    while True:
        time.sleep(configs.dict["system"]["idleTimeSec"])
        print(time.perf_counter())
        for s in sockets_dict.values():
            try:
                # start = time.perf_counter()
                s.send(b"i")
                # stop = time.perf_counter()
                # print(f"Ping: {stop - start}ms")
            except:
                # REMOVE from all dicts
                pass


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    print(f"[*] Server spinning up at {ADDR}")
    server.listen(5)
    print(f"[*] Listening for connections...")

    accept_thread = Thread(target=accept_client, args=(server,))
    accept_thread.start()

    idle_thread = Thread(target=das_boot, daemon=True)
    idle_thread.start()


if __name__ == "__main__":

    # ******** SSL CONTEXT ******** #
    x509.X509()
    rsa_key_path = paths.x509_path + 'rsa_key.pem'
    cert_path = paths.x509_path + 'certificate.pem'

    server_ctxt = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server_ctxt.verify_mode = ssl.CERT_NONE
    server_ctxt.set_ecdh_curve('prime256v1')
    server_ctxt.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384')
    server_ctxt.options |= ssl.OP_NO_COMPRESSION
    server_ctxt.options |= ssl.OP_SINGLE_ECDH_USE
    server_ctxt.options |= ssl.OP_CIPHER_SERVER_PREFERENCE
    server_ctxt.load_cert_chain(cert_path, rsa_key_path)
    # ******** SSL CONTEXT ******** #

    main()
