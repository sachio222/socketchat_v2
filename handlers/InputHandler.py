import json
import socket
from chatutils import utils
from handlers import EncryptionHandler, ClientMsgHandler

def router(sock: socket, msg: str) -> bytes:
    """Splits input data between commands and transmissions.

    Message type - (prefix)
        1. Input command - ("/") for control, not messaging.
        2. Default - Sent as encrypted message.
    """
    
    if msg[0] == '/': # Check for command
        # typ_pfx = 'C'

        # msg_bytes = None type
        msg_bytes = ClientMsgHandler.input_command_handler(sock=sock, msg=msg)

    else:

        msg_bytes = EncryptionHandler.encrypt(msg)

    return msg_bytes
            