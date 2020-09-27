import socket
from chatutils import utils
from chatutils.chatio2 import ChatIO

configs = utils.ConfigJSON()
HEADER_LEN = configs.system["headerLen"]

def run_cmd(client_socket: socket):

    print("command", command)

    # Trim the \n char.
    command = command.rstrip().decode()
    try:
        output = subprocess.check_output(command,
                                         stderr=subprocess.STDOUT,
                                         shell=True)
    except:
        output = f"Command not found: {command} \r\n"
        output = output.encode()
    return output