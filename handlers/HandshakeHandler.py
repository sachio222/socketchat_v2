## GET NAME
## CHECK IF NAME UNIQUE, ACCEPT / REASK
## GENERATE PUBLIC KEYS
## SEND PUBLIC KEYS
from enum import unique
import json
from server2 import onboard_new_client
import socket
from sys import path

from chatutils import utils
from chatutils.chatio2 import ChatIO

from lib.encryption import CipherTools

from handlers import ServMsgHandler, EncryptionHandler

import config.filepaths as paths

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)
users = utils.JSONLoader(paths.user_dict_path)

BUFFER_LEN = configs.system["defaultBufferLen"]
PREFIX_LEN = configs.system["prefixLength"]


class ClientHand(ChatIO):

    def __init__(self, sock: socket):
        self.nick = self.onboard_to_server(sock)
        self.UNIQUE_FLAG = False

    def onboard_to_server(self, sock: socket):
        handshake_payload = {}

        # while not self.UNIQUE_FLAG:
        nick = handshake_payload["nick"] = self.request_nick()
        handshake_payload["public_key"] = self.create_public_key().decode()
        handshake_payload = json.dumps(handshake_payload)
        handshake_payload = handshake_payload.encode()
        self.send_payload(sock, handshake_payload)
        return nick

    def request_nick(self) -> str:
        nick = input("[+] What is your name? ")
        return nick

    def create_public_key(self) -> bytes:
        _, pubk = CipherTools.gen_nacl_key()
        return pubk

    def send_payload(self, sock: socket, payload: bytes):
        self.pack_n_send(sock, prefixes.client["data"], payload)

        # If keys don't exist, make them with encryption
        # Have keys
        # send keys as client["keys"]


class ServerHand(ChatIO):
    def __init__(self, sock, addr):
        self.onboard_new_client(sock, addr)
        # self.addr = addr

    def onboard_new_client(self, sock: socket, addr: tuple):
        print("Client trying to connect...")

        msg_type = sock.recv(PREFIX_LEN)
        new_user = ServMsgHandler.dispatch(sock, msg_type)
        new_user = json.loads(new_user)

        if self.unique_user(new_user):
            self.store_user(addr, new_user)
        else:
            self.resend_prompt(sock)


    def unique_user(self, new_user: dict) -> bool:
        if new_user["nick"] not in users.__dict__.keys():
            return True
        else:
            return False

    def store_user(self,
                addr: tuple,
                new_user: dict,
                nick: str = None,
                public_key: bytes = None,
                trusted: list = None) -> dict:

        """SERVERSIDE USER DICT"""
        # try:
        #     users = utils.JSONLoader(paths.user_dict_path)
        # except Exception as e:
        #     print(f"ERROR: Problem with JSON file at {paths.user_dict_path}. "\
        #         "Check for hanging comma or brackets and stuff.")
        #     exit()

        # new_user = json.loads(new_user)

        # Fill structure with overrides or defaults.
        new_user= {
            "nick": new_user.get("nick", None) or nick,
            "addr": new_user.get("addr", None) or addr,
            "public_key": new_user.get("public_key", None) or public_key,
            "trusted": new_user.get("trusted", None) or trusted
        }
        
        users.__dict__[new_user["nick"]] = new_user
        users.update(paths.user_dict_path)

        return users.__dict__

    
    def resend_prompt(self, sock: socket):
        msg_bytes = b"[x] User already exists. Try something else: "
        self.pack_n_send(sock, prefixes.server["handshake"], msg_bytes)