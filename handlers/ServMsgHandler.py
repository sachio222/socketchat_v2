import socket
from chatutils import utils
from handlers.routers import ServerCmds

configs = utils.JSONLoader()


def dispatch(sock: socket, msg_type: str) -> bytes:
    """Sorts through incoming data by prefix."""
    assert type(msg_type) == bytes, "Convert prefix to str"
    func = ServerCmds.dispatch.get(msg_type.decode(), ServerCmds.error)
    bytes_data = func(sock=sock, msg_type=msg_type)

    return bytes_data
