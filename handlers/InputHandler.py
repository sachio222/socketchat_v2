import socket
from sys import prefix
from chatutils import utils
import config.filepaths as paths
from handlers import EncryptionHandler, ClientMsgHandler

prefixes = utils.JSONLoader(paths.prefix_path)

def dispatch(sock: socket, msg: str) -> bytes:
    """Splits input data between commands and transmissions.

    Message type - (prefix)
        1. Input command - ("/") for control, not messaging.
        2. Default - Sent as encrypted message.
    """
    if len(msg):
        if msg[0] == '/':  # Check for command
            msg = ClientMsgHandler.command_router(sock=sock, msg=msg)
            msg_type = None
        else:
            msg = EncryptionHandler.message_router(msg)
            msg_type = prefixes.dict["client"]["chat"]["msg"]
    else:
        # Send new line on enter press.
        msg = b"\n"
        msg_type = prefixes.dict["client"]["chat"]["newLine"]

    return msg, msg_type
