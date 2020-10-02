import json
import socket
from threading import Thread
from handlers import HandshakeHandler, ServMsgHandler

from chatutils import utils
import config.filepaths as paths

# sys.setrecursionlimit(20000)

configs = utils.JSONLoader()
users = utils.JSONLoader(paths.user_dict_path)

BUFFER_LEN = configs.system["defaultBufferLen"]
PREFIX_LEN = configs.system["prefixLen"]
HOST = configs.system["defaultHost"]
PORT = configs.system["defaultPort"]
ADDR = (HOST, PORT)
socket_list = []


def accept_client(server):
    global users

    while True:
        client_socket, addr = server.accept()
        socket_list.append(client_socket)
        print(f"Connected to {addr}")

        users = HandshakeHandler.ServerSide(client_socket, addr).user

        client_thread = Thread(target=handle_client,
                               args=(client_socket,),
                               daemon=True)
        client_thread.start()
        # utils.delete_user("Will")


def handle_client(client_socket):
    while True:
        msg_type = client_socket.recv(PREFIX_LEN)
        if not msg_type:
            break
        ServMsgHandler.dispatch(client_socket, msg_type)

    client_socket.close()


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
