## GET NAME
## CHECK IF NAME UNIQUE, ACCEPT / REASK
## GENERATE PUBLIC KEYS
## SEND PUBLIC KEYS
import socket
from sys import prefix
from chatutils import utils
from chatutils.chatio2 import ChatIO
from config import filepaths

prefixes = utils.JSONLoader(filepaths.prefix_path)

class User(ChatIO):

    def __init__(self, sock: socket):
        pass

    def request_nick(self, sock: socket) -> str:
        nick = input("[+] What is your name? ")
        self.pack_n_send(sock, prefixes.client["nick"], nick)
