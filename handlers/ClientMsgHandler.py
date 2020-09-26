import socket
from chatutils import utils
from handlers import EncryptionHandler

from handlers.routers import DefaultCmds, AddonCmds, MessageTypes

configs = utils.ConfigJSON()

"""
1. send type in here.
2. route it to the right place.
3. return the message

"""

def input_command_handler(sock: socket, msg: str) -> None:
    """handles input command messages and calls controller funcs.

    All of the controller commands are routed through this function based
    on the presence of a "/" character at the beginning of the command,
    which is detected by the sender function. Each command has a different
    end point and they all behave differently depending on their defined
    purposes.

    Args
        msg - (Usually str) - the raw input command before processing.
    """
    # 1. Convert to string if needed.
    if type(msg) == bytes:
        msg.decode()

    # 2. Split msg into command and keywords
    msg_parts = msg.split(' ')
    
    # 3. Search through commands for function, starting with default commands.

    name_spaces = [DefaultCmds, AddonCmds]

    for name_space in name_spaces:
        func = name_space.dispatch_cmds.get(msg_parts[0], False)
        print(func)
        if func:
            break
    try:
        func(sock=sock, msg_parts=msg_parts)
    except Exception as e:
        print(e)
        print(f'-!- {msg_parts[0]} is not a valid command.')

    return None

d
