import os
import sys
import socket

from chatutils import utils

configs = utils.ConfigJSON()

class ChatIO:
    def __init__(self):
        pass
    def pack_n_send(self, sock: socket, typ_pfx: str, data: str) -> None:
        """Convenience function, packs data and sends data."""
        data = self.pack_data(typ_pfx, data)
        sock.send(data)
    

    def pack_data(self, typ_pfx:str, data:str) -> bytes:
        """
        Example packet:
            
        """
        if typ_pfx == "M":
            size = len(data)
        header = f'{size:<{configs.system["headerLen"]}}'
        packed_data = f"{typ_pfx}{header}{data}"
        return packed_data.encode()
