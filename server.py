#!/usr/bin/ python3

import socket
import sys
from threading import Thread

import chatutils.xfer as xfer
import chatutils.utils as utils
from chatutils.chatio import ChatIO
from chatutils.channel import Channel 

sockets = {}
nicks_by_sock = {}
addrs_by_nick = {}

class Server(ChatIO, Channel):
    """Server class"""
    def __init__(self):
        super(Server, self).__init__()
        self.BFFR = 1

    def accepting(self):
        # Accept connections.
        while True:
            client_cnxn, client_addr = sock.accept()
            print(f'-+- Connected... to {client_addr}')
            sockets[client_cnxn] = client_addr  # Create cnxn:addr pairings.
            Thread(target=self.handle_clients, args=(client_cnxn,)).start()

    def handle_clients(self, client_cnxn):
        # Get username.
        user_name = self.init_client_data(client_cnxn)
        self.pack_n_send(client_cnxn, 'M', f"{user_name} is in the house!")

        # Start listening.
        while True:
            data = client_cnxn.recv(self.BFFR)  # Receive data as chunks.

            if not data:
                #TODO: Run through connected sockets, clean up list.
                del (addrs_by_nick[nicks_by_sock[client_cnxn]])
                print('addrs_by_nick: ', addrs_by_nick)
                del (nicks_by_sock[client_cnxn])
                print('nicks_by_sock: ', nicks_by_sock)
                del (sockets[client_cnxn])  # remove address
                print('sockets: ', sockets)

                break

            self.data_router(client_cnxn, data)

    def data_router(self, client_cnxn, data):
        # Server client communication codes.

        # Send confirm dialog to recip if user is sending file.
        if data == "/".encode():
            print('controller')
            # Drain socket of controller message so it doesn't print.
            control = self.unpack_msg(client_cnxn).decode()
            
            if control == 'status':
                status = self.get_status(addrs_by_nick)
                print(status)

            print('control is',control)

        # U-type handler
        if data == b'U':  # 85 = U
            self._serv_u_hndlr(client_cnxn)

        else:
            # Reattach prefix before sending to server.
            # print('data is', data)
            buff_text = client_cnxn.recv(4096)
            # print('buffer text is', buff_text)
            data = data + buff_text
            # print('combined they are', data)
            for sock in sockets:
                if sockets[sock] != sockets[client_cnxn]:
                    # print(sock)
                    try:
                        sock.send(data)

                    except:
                        pass

        # General print to server.
        # print('>> ', data.decode())

    def _serv_u_hndlr(self, sock):
        """ handles user requests
        If U-type is received from sender, initiate this method.
        1 .check if user is here. if not, send new prompt.
        
        """
        username = self.unpack_msg(sock)
        print(username)
        if username != b'cancel':

            # Check for address.
            match, user_addr = self.lookup_user(sock, username)

            # Send U type to sender.
            self.pack_n_send(sock, 'U', str(match))
        else:
            cancel_msg = 'x-x Send file cancelled. Continue chatting.'
            self.pack_n_send(sock, 'M', cancel_msg)

    def lookup_user(self, sock, user_query):
        """Checks if user exists. If so, returns user and address.

        Args: 
            sock: (socket) Incoming socket object (from sender)
            user_query: (str) Name of user to look up.
        
        Returns
            match: (bool) True if user found
            user_addr: (str) ip:port of user.
        """
        match = False
        user_addr = ''

        try:
            user_query = user_query.decode()
        except:
            pass

        for nick, addr in addrs_by_nick.items():
            if addr != sockets[sock]:  # Avoid self match.

                if nick == user_query:
                    match = True
                    user_addr = addr

                    break

                else:
                    match = False

        return match, user_addr

    def init_client_data(self, sock):
        """Sets nick and addr of user."""
        unique = False
        PROMPT = '-+- Enter nickname:'

        self.pack_n_send(sock, 'M', PROMPT)
        while not unique:
            # sock.recv(1)  # Shed first byte.
            user_name = self.unpack_msg(sock, shed_byte=True).decode()

            if user_name not in nicks_by_sock.values():
                nicks_by_sock[sock] = user_name  # Create socket:nick pair.
                addrs_by_nick[user_name] = sockets[
                    sock]  # Create nick:addr pair.
                unique = True
            else:
                ERR = f"=!= They're already here! Pick something else:"
                print(ERR)
                self.pack_n_send(sock, 'M', ERR)

        # TODO: Fix formatting.
        return user_name

    def start(self):
        Thread(target=self.accepting).start()


if __name__ == "__main__":
    # TODO: Add inputs.
    server = Server()

    addy = ('127.0.0.1', 1515)
    sock = socket.socket()
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addy)
    except Exception as e:
        print(f'-x- {e}')
        utils.countdown(90)

    sock.listen(5)
    print(f'-+- Listening...')
    server.start()
