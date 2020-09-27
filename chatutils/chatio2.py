import os
import sys
import socket
from chatutils import utils

configs = utils.JSONLoader()

HEADER_LEN = configs.system["headerLen"]


class ChatIO:

    def __init__(self):
        pass

    def pack_n_send(self, sock: socket, typ_pfx: str, data: str) -> None:
        """Convenience function, packs data and sends data."""
        data = self.pack_data(typ_pfx, data)
        sock.send(data)

    def pack_data(self, typ_pfx: str, data: str) -> bytes:
        """
        Example packet:
            
        """
        try:
            data = data.decode()
        except:
            pass

        data = data + "\n"

        # if typ_pfx == "M":
        size = len(data)

        header = f'{size:<{configs.system["headerLen"]}}'
        packed_data = f"{typ_pfx}{header}{data}"
        return packed_data.encode()

    @classmethod
    def unpack_data(cls, sock: socket) -> bytes:
        """UNPACK DATA"""
        msg_len = sock.recv(HEADER_LEN)
        msg = sock.recv(int(msg_len))
        msg = msg.rstrip()
        return msg

    @classmethod
    def broadcast(cls, sock: socket, socket_dict: dict):
        print(socket_dict)
