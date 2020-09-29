import socket
from threading import Thread
from handlers import ServMsgHandler

from chatutils import utils
import config.filepaths as paths

# sys.setrecursionlimit(20000)

configs = utils.JSONLoader()

BUFFER_LEN = configs.system["defaultBufferLen"]
PREFIX_LEN = configs.system["prefixLength"]
HOST = configs.system["defaultHost"]
PORT = configs.system["defaultPort"]
ADDR = (HOST, PORT)
socket_list = []


def accept_client(server):
    while True:
        client_socket, addr = server.accept()

        onboard_new_client(client_socket, addr)

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


def onboard_new_client(client_socket: socket, addr: tuple):
    print("Client trying to connect...")

    socket_list.append(client_socket)

    msg_type = client_socket.recv(PREFIX_LEN)

    user_dict = ServMsgHandler.dispatch(client_socket, msg_type)
    
    print("user_dict: ", user_dict)
    # user_dict = utils.store_user(client_socket, addr, nick=user_dict)

    print(f"Connected to {addr}")
    welcome_msg = f"Welcome to {ADDR}"

    client_socket.send(welcome_msg.encode())


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
