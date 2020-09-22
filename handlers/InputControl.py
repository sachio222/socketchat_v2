import json
from pathlib2 import Path
from chatutils import utils
from handlers.routers import default, addons


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

    # 3. Check through default command dict.
    self_name = default
    func = self_name.Router().cmd_dict.get(msg_parts[0], False)

    if not func:
        # 4. If no value, check through addons command dict.
        self_name = addons
        func = self_name.Router().cmd_dict.get(msg_parts[0], False)

    # 5. Run command, passing self, msg_parts, sock, or Fail.
    if func:
        func(self_name.Router, msg_parts, sock)

    else:
        print('-!- Not a valid command.')

def message_type_handler():
    pass