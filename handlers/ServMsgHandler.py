import socket
from chatutils import utils
from handlers.routers import ServerCmds

configs = utils.JSONLoader()


def dispatch(sock: socket, buffer: dict) -> bytes:
    """Sorts through incoming data by prefix."""
    assert type(buffer["msg_type"]) == bytes, "Convert prefix to str"
    func = ServerCmds.dispatch.get(buffer["msg_type"].decode(),
                                   ServerCmds.error)
    bytes_data = func(sock=sock, buffer=buffer)

    return bytes_data
