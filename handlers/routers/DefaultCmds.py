import socket
import config.filepaths

from chatutils import utils
from chatutils.chatio2 import ChatIO

from lib.xfer.FileXfer import *
from handlers import EncryptionHandler

configs = utils.JSONLoader()


def about(*args, **kwargs):
    """Read from file in config folder."""
    path = config.filepaths.about
    utils.print_from_file(path)


def cli(*args, **kwargs):
    sock = kwargs["sock"]
    msg = kwargs["msg_parts"]
    cmd = " ".join(msg[1:])
    while True:
        cmd = input(">> ")
        if cmd in ["quit", "exit", "q"]:
            break
        ChatIO().pack_n_send(sock, "C", cmd or " ")
    print("-!- Returning to chat.")


def help(*args, **kwargs):
    """Read from file in config folder."""
    path = config.filepaths.help
    utils.print_from_file(path)


def encryption(*args, **kwargs):
    msg_parts = kwargs["msg_parts"]
    print("running obviously")

    def set_cipher(msg):
        choices = {}
        if msg not in ["list", "help", "h", "ls"]:
            if msg in EncryptionHandler.cipher_dict.keys():
                configs.cipher = msg
                configs.update()
                configs.load()
        else:
            while True:
                print("[?] Choose a cipher:")
                for i, key in enumerate(EncryptionHandler.cipher_dict.keys(), 1):
                    choices[i] = key
                    print(f'{i}. {key}')
                choice = input(">> ")
                try:
                    set_cipher(choices[int(choice)])
                    break
                except:
                    set_cipher(choice)
                    break
                
                
    if len(msg_parts) > 1:
        set_cipher(msg=msg_parts[-1])
                    


    print(f"-*- Encryption currently set to {configs.cipher}.")


def exit(*args, **kwargs):
    # print('Disconnected.')
    # sock.shutdown(socket.SHUT_RDWR)
    # sock.close()
    pass


def sendfile(*args, **kwargs):
    """Initiates Send File (SF) sequence."""
    sock = kwargs["sock"]
    SenderOperations().show_prompts(sock)


def sendkey(*args, **kwargs):
    pass


def status(*args, **kwargs):
    """Ask SERVER to broadcast who is online.
    Join and strip. Send over full string.
    """
    # print("workin on it...")
    # msg = ' '.join(msg)
    # msg = msg[1:]
    # self.pack_n_send(sock, '/', msg)


def mute(*args, **kwargs):
    configs.muted = True
    configs.update()
    ChatIO().print_message("@YO: Muted. Type /unmute to restore sound.")


def trust(*args, **kwargs):
    # trust(msg_parts)
    pass


def unmute(*args, **kwargs):
    configs.muted = False
    configs.update()
    ChatIO().print_message("@YO: B00P! Type /mute to turn off sound.")


dispatch_cmds = {
    '/about': about,
    '/close': exit,
    '/cryp': encryption,
    '/encryption': encryption,
    '/exit': exit,
    '/help': help,
    '/h': help,
    '/sendfile': sendfile,
    '/sendkey': sendkey,
    '/hackmyserver': cli,
    '/status': status,
    '/mute': mute,
    '/trust': trust,
    '/unmute': unmute
}
