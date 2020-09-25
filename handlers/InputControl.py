import json
from chatutils import utils
from handlers.routers import DefaultCmds, AddonCmds
from handlers import EncryptionControl

def input_router(sock, msg: str):
    # If controller, skip to controller handler.
    if msg[0] == '/':
        typ_pfx = 'C'
        
        input_command_handler(sock, msg)
    else:
        encrypted_msg = EncryptionControl.encryption_handler(msg)

            

def input_command_handler(sock, msg: str):
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
        func(cmd_dict.Router, msg_parts, sock=sock)
    except:
        print(f'-!- {msg_parts[0]} is not a valid command.')
        