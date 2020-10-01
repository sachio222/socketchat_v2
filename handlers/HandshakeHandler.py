## GET NAME
## CHECK IF NAME UNIQUE, ACCEPT / REASK
## GENERATE PUBLIC KEYS
## SEND PUBLIC KEYS



from enum import unique
import json
# from server2 import onboard_new_client
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
PREFIX_LEN = configs.system["prefixLen"]


class ClientHand(ChatIO):

    def __init__(self, sock: socket):
        self.sock = sock
        self.nick = self.onboard_to_server()

    def onboard_to_server(self):
        handshake_payload = {}
        data = self.revc_n_unpack(self.sock, shed_pfx=True)

        print(data)
        


        # nick = handshake_payload["nick"] = self.request_nick()
        # handshake_payload["public_key"] = self.create_public_key().decode()
        # handshake_payload = json.dumps(handshake_payload)
        # handshake_payload = handshake_payload.encode()
        # self.send_payload(sock, handshake_payload)
        return nick

    def request_nick(self) -> str:
        # nick = input("[+] What is your name? ")
        # return nick
        pass

    def create_public_key(self) -> bytes:
        _, pubk = CipherTools.gen_nacl_key()
        return pubk

    def send_payload(self, sock: socket, payload: bytes):
        self.pack_n_send(sock, prefixes.client["chat"]["data"], payload)

        # If keys don't exist, make them with encryption
        # Have keys
        # send keys as client["keys"]


class ServerHand(ChatIO):

    def __init__(self, sock, addr):
        self.sock = sock
        self.onboard_new_client(addr)
        # self.addr = addr

    def onboard_new_client(self, addr: tuple):
        print("Client trying to connect...")
        self.set_client_data()


        # msg_type = self.sock.recv(PREFIX_LEN)
        # new_user = ServMsgHandler.dispatch(self.sock, msg_type)
        # new_user = json.loads(new_user)

        # if not self.unique_user(new_user):
        #     self.resend_prompt(self.sock)
        # else:
        #     self.store_user(addr, new_user)
        # self.send_welcome(self.sock)

    def set_client_data(self):
        unique = False
        self.send_nick_prompt()
        
        while not unique:
            user_name = self.revc_n_unpack(self.sock, shed_pfx_len=PREFIX_LEN)
            print(user_name)



    def unique_user(self, new_user: dict) -> bool:
        if new_user["nick"] not in users.__dict__.keys():
            return True
        else:
            return False

    def send_nick_prompt(self):
        self.pack_n_send(self.sock, prefixes.server["handshake"]["nick"], configs.msgs["getNick"])
        

    def resend_prompt(self):
        msg_bytes = b"[x] User already exists. Try something else: "
        self.pack_n_send(self.sock, prefixes.server["chat"]["handshake"], msg_bytes)
    
    
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
        new_user = {
            "nick": new_user.get("nick", None) or nick,
            "addr": new_user.get("addr", None) or addr,
            "public_key": new_user.get("public_key", None) or public_key,
            "trusted": new_user.get("trusted", None) or trusted
        }

        users.__dict__[new_user["nick"]] = new_user
        users.update(paths.user_dict_path)

        return users.__dict__


    def send_welcome(self):
        self.pack_n_send(self.sock, prefixes.server["handshake"]["welcome"],
                         configs.msgs["welcome"])
