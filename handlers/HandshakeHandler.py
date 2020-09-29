## GET NAME
## CHECK IF NAME UNIQUE, ACCEPT / REASK
## GENERATE PUBLIC KEYS
## SEND PUBLIC KEYS
import socket

from chatutils import utils
from chatutils.chatio2 import ChatIO

from lib.encryption import CipherTools

from handlers import EncryptionHandler

import config.filepaths as paths

prefixes = utils.JSONLoader(paths.prefix_path)


class UserHandshake(ChatIO):

    def __init__(self, sock: socket):
        self.handshake_payload = {}
        self.handshake_payload["nick"] = self.request_nick()
        self.handshake_payload["pubk"] = self.create_public_key().decode()
        self.send_payload(sock)

    def request_nick(self) -> str:
        print("prefix is:", prefixes.client)
        nick = input("[+] What is your name? ")
        return nick

    def check_uniqueness(self, nick: str, namedict: dict):
        unique = False
        # name_dict
        return unique

    def create_public_key(self) -> bytes:
        _, pubk = CipherTools.gen_nacl_key()
        return pubk

    def send_payload(self, sock: socket):
        self.pack_n_send(sock, prefixes.client["hshk"], self.handshake_payload.encode())

        # If keys don't exist, make them with encryption
        # Have keys
        # send keys as client["keys"]


class Server(ChatIO):
    def __init__(self):
        pass

    def receive_nick(self):
        pass
