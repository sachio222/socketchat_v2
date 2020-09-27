import socket
import subprocess

from chatutils import utils
from chatutils.chatio2 import ChatIO

configs = utils.JSONLoader()
HEADER_LEN = configs.system["headerLen"]

def commands(client_socket):
    # while True:
    client_socket.send(b"<<cmd:#>> ")
    cmd_buffer = ChatIO.unpack_data(client_socket)
    response = run_cmd(cmd_buffer)
    client_socket.send(response)

def run_cmd(command) -> bytes:
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


