import json
import socket
from types import ModuleType
from chatutils import utils
import config.filepaths as paths

configs = utils.JSONLoader()
prefixes = utils.JSONLoader(paths.prefix_path)
users = utils.JSONLoader(paths.user_dict_path)

PREFIX_LEN = configs.dict["system"]["prefixLen"]
HEADER_LEN = configs.dict["system"]["headerLen"]


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



        size = len(data)

        utils.debug_(size, "size", "pack_n_send")
        header = self._make_header(size)

        packed_data = f"{typ_pfx}{header}{data}"
        # utils.debug_(packed_data, "packed_data", "pack_data", override=True)
        return packed_data.encode()

    def _make_header(self, size: int, header_len: int = HEADER_LEN):
        header = f'{size:<{header_len}}'
        return header

    def recv_n_unpack(self, sock: socket, shed_pfx: bool = False) -> bytes:
        if shed_pfx:
            # Dump bytes into the ether.
            sock.recv(PREFIX_LEN)
        data = self.unpack_data(sock)
        return data

    def recv_n_dispatch(self, sock: socket, cmd_module: ModuleType) -> bytes:
        """Gets type and dispatches to proper command module"""
        msg_type = sock.recv(PREFIX_LEN)
        bytes_data = self.dispatch(sock, msg_type, cmd_module)
        return bytes_data

    def dispatch(self, sock: socket, msg_type: str,
                 cmd_module: ModuleType) -> bytes:
        """Sorts through incoming data by prefix."""
        assert type(msg_type) == bytes, "Convert prefix to str"
        func = cmd_module.dispatch.get(msg_type.decode(), cmd_module.error)
        bytes_data = func(sock=sock, msg_type=msg_type)

        return bytes_data

    @classmethod
    def unpack_data(cls, sock: socket) -> bytes:
        """UNPACK DATA"""
        msg_len = sock.recv(HEADER_LEN)
        utils.debug_(msg_len, "msg_len", "unpack_data")
        try:
            msg_bytes = sock.recv(int(msg_len))
        except:
            msg_bytes = ""

        # msg = msg.rstrip()
        return msg_bytes

    @staticmethod
    def make_buffer(sockets_dict: dict, user_dict: dict, msg_type: bytes) -> dict:
        buffer = {}
        buffer["sender_nick"] = user_dict["nick"]
        buffer["sockets"] = sockets_dict
        buffer["msg_type"] = msg_type
        buffer["msg_bytes"] = ""
        return buffer

    def add_sender_nick(self, buffer: dict) -> bytes:
        send_buffer = {}
        # utils.debug_(buffer, "buffer", "RAW buffer DICT", override=False)
        sender_nick = buffer["sender_nick"]
        send_buffer = json.loads(buffer["msg_bytes"])
        # utils.debug_(buffer, "buffer", "BUFFER AFTER JSON LOADS", override=False)
        send_buffer["sender"] = sender_nick
        msg_bytes = json.dumps(send_buffer)
        # msg_bytes = f"@{sender_nick}: {msg_bytes}"
        return msg_bytes.encode()

    def add_system_handle(self, buffer: dict) -> bytes:
        send_buffer = {}
        system_nick = configs.dict["system"]["sysNick"]
        send_buffer["msg_pack"] = buffer["msg_bytes"]
        send_buffer["sender"] = system_nick
        utils.debug_(send_buffer, "send_buffer", "AFTER NICK ADDED", override=False)
        
        # print(buffer)
        return send_buffer


    def broadcast(self, send_sock: socket, buffer: dict, cast_type: "str" = None):
        if cast_type == "sys":
            msg_bytes = self.add_system_handle(buffer)
        else:
            msg_bytes = self.add_sender_nick(buffer)
            print(msg_bytes.decode())
        sockets = buffer["sockets"]
        for s in sockets.values():
            if s != send_sock:
                self.pack_n_send(s, prefixes.dict["server"]["chat"]["default"], msg_bytes)

    def print_to_client(self, data_dict: dict):
        # print(f'@{data_dict["sender"]}: {data_dict["msg_pack"]}')
        print(f'@{data_dict["sender"]}: {data_dict["msg_pack"]["ciphertext"]}')
