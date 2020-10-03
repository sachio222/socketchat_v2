import socket
from threading import Thread, active_count
from handlers import HandshakeHandler, ServMsgHandler

from chatutils import utils
from chatutils.chatio2 import ChatIO

import config.filepaths as paths

configs = utils.JSONLoader()
users = utils.JSONLoader(paths.user_dict_path)
users.clear()

BUFFER_LEN = configs.dict["system"]["defaultBufferLen"]
PREFIX_LEN = configs.dict["system"]["prefixLen"]
HOST = configs.dict["system"]["defaultHost"]
PORT = configs.dict["system"]["defaultPort"]
ADDR = (HOST, PORT)
sockets_dict = {}
active_sockets = []

def accept_client(server):

    while True:
        client_socket, addr = server.accept()
        active_sockets.append(client_socket)
        idle_thread = Thread(target=das_boot, daemon=True)
        idle_thread.start()
        
        print(f"[+] Connected to {addr}")

        client_thread = Thread(target=handle_client,
                               args=(client_socket, addr ),
                               daemon=True)
        client_thread.start()


def handle_client(client_socket:socket , addr: tuple) -> None:

    user_dict = HandshakeHandler.ServerSide(client_socket, addr).user
    print(f"[+] {user_dict['nick']} has joined the chat.")
    
    sockets_dict[user_dict["nick"]] = client_socket
    
    while True:
        msg_type = client_socket.recv(PREFIX_LEN)

        if not msg_type:
            del sockets_dict[user_dict["nick"]]
            utils.delete_user(user_dict["nick"])
            break

        buffer = ChatIO.make_buffer(sockets_dict, user_dict, msg_type)

        ServMsgHandler.dispatch(client_socket, buffer)

    client_socket.close()

def das_boot():
    import time
    while True:
        time.sleep(configs.dict["system"]["idleTimeSec"])
        print(time.perf_counter())
        for s in sockets_dict.values():
            try:
                start = time.perf_counter()
                s.send(b"i")
                stop = time.perf_counter()
                print(f"Ping: {stop - start}ms")
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


if __name__ == "__main__":
    main()
