import json
import socket
from chatutils import utils
from handlers.routers import DefaultCmds, AddonCmds
from handlers import EncryptionHandler, MessageHandler

def input_router(sock: socket, msg: str) -> bytes:
    """Splits input data between commands and transmissions.

    Message type - (prefix)
        1. Input command - ("/") for control, not messaging.
        2. Default - Sent as encrypted message.
    """

    if msg[0] == '/': # Check for command
        # typ_pfx = 'C'

        # msg_bytes = None type
        msg_bytes = MessageHandler.input_command_handler(sock=sock, msg=msg)

    else:

        msg_bytes = EncryptionHandler.Handler().encryption_handler(msg)

    return msg_bytes
            