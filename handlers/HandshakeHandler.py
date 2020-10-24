import socket, json
from chatutils import utils, channel2
from chatutils.chatio2 import ChatIO
from lib.encryption import CipherTools

from handlers.routers import HandshakeCmds

import config.filepaths as paths
configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)
users = utils.JSONLoader(paths.user_dict_path)

BUFFER_LEN = configs.dict["system"]["bufferLen"]
PREFIX_LEN = configs.dict["system"]["prefixLen"]


class ClientSide(ChatIO):

    def __init__(self, sock: socket):
        self.sock = sock
        self.nick = self.onboard_to_server()

    def onboard_to_server(self) -> str:
        nick = ""
        unique = "False"  # Can't send bool over socket.

        while unique == "False":
            try:
                # 1. Receive server prompt
                prompt = self.recv_n_unpack(self.sock, shed_pfx=True).decode()

                # 2. Pack payload (user, keys, etc)
                payload, nick = self._create_payload(prompt)

                # 3. Send Payload.
                self.send_payload(self.sock, payload)

                # 4. Receive uniqueness.
                unique = self.recv_n_unpack(self.sock, HandshakeCmds).decode()
                if not unique:
                    channel2.killit()
                    break
            except:
                pass
        return nick

    def show_nick_request(self, prompt: str) -> str:
        nick = ""
        valid_nick = False

        while not valid_nick:
            nick = input(prompt)
            valid_nick = self.is_valid(nick)
    
        return nick

    def is_valid(self, nick: str) -> bool:
        if nick not in [""]:
            return True
        else:
            print(configs.dict["msg"]["getNickErr"])
            return False

    def _create_payload(self, prompt: str) -> tuple:
        handshake_payload = {}
        nick = handshake_payload["nick"] = self.show_nick_request(prompt)
        handshake_payload["public_key"] = self.create_public_key().decode()
        print("[+] New NACL keys generated.")
        handshake_payload["verify_key"] = self.create_verify_key().decode()
        print("[+] New NACL signing keys generated.")
        handshake_payload = json.dumps(handshake_payload)
        handshake_payload = handshake_payload.encode()
        return handshake_payload, nick

    def create_public_key(self) -> bytes:
        _, pubk, _, _ = CipherTools.gen_nacl_key()
        return pubk

    def create_verify_key(self) -> bytes:
        _, _, _, vfyk = CipherTools.gen_nacl_key()
        return vfyk

    def send_payload(self, sock: socket, payload: bytes):
        self.pack_n_send(sock, prefixes.dict["client"]["chat"]["data"], payload)


class ServerSide(ChatIO):

    users.reload()

    def __init__(self, sock: socket, addr: tuple):
        self.sock = sock
        self.addr = addr
        self.user = self.onboard_new_client()

    def onboard_new_client(self):
        user = ""
        first_request = True
        unique = "False"

        print("[/] Client trying to connect...")

        while unique == "False":

            # 1. Get nick
            if first_request:
                user = self.send_nick_request()
                first_request = False   
            else:
                user = self.resend_nick_request()
            user = json.loads(user)

            # 2. Check if Unique
            unique = self.is_unique(user)

        self.store_user(self.addr, user)
        self.send_welcome_msg()
        return user

    def send_nick_request(self) -> bytes:
        # Goes to handler
        self.pack_n_send(self.sock, prefixes.dict["server"]["handshake"]["nick"],
                         configs.dict["msg"]["getNick"])
        user_json = self.recv_n_unpack(self.sock, shed_pfx=True)
        return user_json

    def resend_nick_request(self):
        self.pack_n_send(self.sock, prefixes.dict["server"]["handshake"]["nick"],
                         configs.dict["msg"]["getNickAgain"])
        user_json = self.recv_n_unpack(self.sock, shed_pfx=True)
        return user_json

    def is_unique(self, new_user: dict) -> bool:
        users.reload()

        try:
            if new_user["nick"] not in users.dict.keys():
                unique = "True"
            else:
                unique = "False"
        except:
            unique = "True"

        self.pack_n_send(self.sock, prefixes.dict["server"]["handshake"]["unique"],
                         unique.encode())
        return unique

    def send_welcome_msg(self):
        self.pack_n_send(self.sock, prefixes.dict["server"]["handshake"]["welcome"],
                         configs.dict["msg"]["welcome"])

    def store_user(self,
                   addr: tuple,
                   new_user: dict,
                   nick: str = None,
                   public_key: bytes = None,
                   verify_key: bytes = None,
                   trusted: list = None) -> dict:
        """SERVERSIDE USER DICT"""

        new_user = {
            "nick": new_user.get("nick", None) or nick,
            "addr": new_user.get("addr", None) or addr,
            "public_key": new_user.get("public_key", None) or public_key,
            "verify_key": new_user.get("verify_key", None) or verify_key,
            "trusted": new_user.get("trusted", None) or trusted
        }

        users.dict[new_user["nick"]] = new_user
        users.update()

        return users.dict
