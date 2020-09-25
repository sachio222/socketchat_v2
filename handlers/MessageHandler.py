import socket
from chatutils import utils
from handlers.routers import DefaultCmds, AddonCmds

configs = utils.ConfigJSON()

"""
1. send type in here.
2. route it to the right place.
3. return the message

"""

def input_command_handler(sock: socket, msg: str) -> None:
    """Sorts through input command messages and calls controller funcs.

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

    cmd_dicts = [DefaultCmds, AddonCmds]

    for cmd_dict in cmd_dicts:
        func = cmd_dict.Router().dispatch_cmds.get(msg_parts[0], False)
        if func:
            break
    try:
        func(cmd_dict.Router, sock=sock, msg=msg_parts)
    except:
        print(f'-!- {msg_parts[0]} is not a valid command.')

    return None

class MessageRouter():
    def __init__(self):
        pass

    def message_type_handler():
        pass

    def transmit():
        pass

    dispatch_cmds = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "e": None,
        "f": None,
        "g": None,
        "h": None,
        "i": None,
        "j": None,
        "k": None,
        "l": None,
        "m": None,
        "n": None,
        "o": None,
        "p": None,
        "q": None,
        "r": None,
        "s": None,
        "t": None,
        "u": None,
        "v": None,
        "w": None,
        "x": None,
        "y": None,
        "z": None,
        "A": None,
        "B": None,
        "C": None,
        "D": None,
        "E": None,
        "F": None,
        "G": None,
        "H": None,
        "I": None,
        "J": None,
        "K": None,
        "L": None,
        "M": transmit,
        "N": None,
        "O": None,
        "P": None,
        "Q": None,
        "R": None,
        "S": None,
        "T": None,
        "U": None,
        "V": None,
        "W": None,
        "X": None,
        "Y": None,
        "Z": None,
        "/": None
    }