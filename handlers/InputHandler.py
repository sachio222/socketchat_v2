import socket
from chatutils import utils
from handlers import EncryptionHandler, ClientMsgHandler


def dispatch(sock: socket, msg: str) -> bytes:
    """Splits input data between commands and transmissions.

    Message type - (prefix)
        1. Input command - ("/") for control, not messaging.
        2. Default - Sent as encrypted message.
    """
    if len(msg):
        if msg[0] == '/':  # Check for command
            msg_bytes = ClientMsgHandler.input_command_handler(sock=sock,
                                                               msg=msg)
        else:
            msg_bytes = EncryptionHandler.encrypt(msg)
    else:
        msg_bytes = "\n"

    return msg_bytes
