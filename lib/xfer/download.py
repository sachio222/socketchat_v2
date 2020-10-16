import os, sys, socket

from chatutils.chatio2 import ChatIO

from chatutils import utils
configs = utils.JSONLoader()

BUFFER_LEN = configs.dict["system"]["bufferLen"]

def write(sock:socket, target_path:str = 'testfile1.jpg'):
    """WRITE FILE TO TARGET_PATH FROM SOCK"""
    while True:
        print("[<==] Downloading...")
        file_buffer = b""
        recv_len = 1

        try:
            while recv_len:
                data = sock.recv(BUFFER_LEN)
                recv_len = len(data)

                if not data:
                    break

                # Overwrite file if exists.
                with open(target_path, 'wb') as f:
                    f.write(data)

                if recv_len < BUFFER_LEN:
                    print("[*] File successfully downloaded.")
                    # print(f"breaking 1. because recv_len is {recv_len}")
                    break

                else:
                    with open(target_path, 'ab') as f:
                        while True:
                            data = sock.recv(BUFFER_LEN)
                            recv_len = len(data)

                            # Append rest of data chunks
                            f.write(data)

                            if recv_len < BUFFER_LEN:
                                print("[*] File successfully downloaded.")
                                # print(f"breaking 2 because recv_len is {recv_len}")
                                break

                # ChatIO().pack_n_send(sock, "M", '{"msg_pack": {"cipher_text": "DONE"}}')
                ChatIO().pack_n_send(sock, "S", "[!] File transferred successfully.")
                break
                
        except:
            ChatIO().pack_n_send(sock, "S", "[x] File transfer failed")

        break

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
            write_file(sock, path, recv_len, "ab")
