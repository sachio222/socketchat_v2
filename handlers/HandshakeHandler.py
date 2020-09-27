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


class User(ChatIO):

    def __init__(self, sock: socket):
        self.send_keys()

    def request_nick(self, sock: socket) -> str:
        nick = input("[+] What is your name? ")
        self.pack_n_send(sock, prefixes.client["nick"], nick)

    def check_uniqueness(self, nick: str, namedict: dict):
        unique = False
        # name_dict
        return unique

    def send_keys(self):
        CipherTools.gen_nacl_key()

        # If keys don't exist, make them with encryption
        # Have keys
        # send keys as client["keys"]
