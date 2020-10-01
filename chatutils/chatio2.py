import json
import socket
from chatutils import utils

configs = utils.JSONLoader()

HEADER_LEN = configs.system["headerLen"]
PREFIX_LEN = configs.system["prefixLen"]



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

        # data = data + "\n"
        size = len(data)
        header = self._make_header(size)
        packed_data = f"{typ_pfx}{header}{data}"
        return packed_data.encode()

    def _make_header(self, size:int, header_len: int = HEADER_LEN):
        header = f'{size:<{header_len}}'
        return header


    def revc_n_unpack(self, sock:socket, shed_pfx_len: int = 0) -> bytes:
        if shed_pfx_len:
            # Dump bytes into the ether.
            sock.recv(shed_pfx_len)
        data = self.unpack_data(sock)
        return data
        

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
