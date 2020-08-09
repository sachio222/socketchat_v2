#!/usr/bin/python3
"""Encryptochat 2.0"""

import os
import sys
import socket
from threading import Thread
import argparse

import cryptography

from chatutils import utils
from chatutils.xfer import FileXfer
from chatutils.chatio import ChatIO
from chatutils.channel import Chime


class Client(ChatIO):
    def __init__(self, muted=False):
        super(Client, self).__init__()
        self.muted = muted
        self.message_type = 'M'
        self.msg = ''
        self.filesize = ''
        self.path = ''

    #===================== SENDING METHODS =====================#
    def sender(self):
        """Accepts user input, checks type, and begins sending to recip.

        Accepts input, and checks if it's a command. If it's prefixed with a
        '/'. Then it is routed to the inp_ctrl_handler where different
        controls are mapped. If it doesn't begin with '/', it's treated as a
        generic message. 
        """
        while True:
            self.msg = input('')
            if self.msg:
                if self.msg[0] == '/':
                    typ_pfx = 'C'
                    self.inp_ctrl_handler(self.msg)
                else:
                    typ_pfx = self.message_type
                    self.pack_n_send(serv_sock, typ_pfx, self.msg)
            else:
                self.msg = ''

            self.message_type = 'M'  # Always reset to default.

    def inp_ctrl_handler(self, msg):
        """Sorts through input control messages and calls controller funcs."""
        if type(msg) == bytes:
            msg.decode()

        if msg == '/about':
            path = 'config/about.txt'
            utils.print_from_file(path)

        elif msg == '/help' or msg == '/h':
            # Print help menu
            path = 'config/helptxt.txt'
            utils.print_from_file(path)

        elif msg == '/sendfile' or msg == '/sf':
            # For sending file. Call send dialog.
            self.path, self.filesize = xfer.sender_prompt()
            if self.path:
                xfer.user_prompt(serv_sock)
        
        elif msg == '/status':
            # Get room status.
            self.pack_n_send(serv_sock, '/', 'status')
        
        elif msg == '/mute':
            self.muted = True
            self.print_message("YO: Muted. Type /unmute to restore sound.")
            
        
        elif msg =='/unmute':
            self.muted = False
            self.print_message("YO: B00P! Type /mute to turn off sound.")


        else:
            print('-!- Command not recognized.')

    #===================== RECEIVING METHODS =====================#
    def receiver(self):
        """A Threaded socket that calls a function to check message type."""
        while True:
            typ_pfx = serv_sock.recv(1)
            if not typ_pfx:
                serv_sock.close()
                print("-!- Aw, snap. Server's disconnected.")
                break
            self._inb_typ_hndlr(typ_pfx)

    def _inb_typ_hndlr(self, typ_pfx):
        """Called by Receiver. Routes messages based on message type.
        
        Checks messages for type. M is standard message. F is sending a file.
                C is for a controller message. A is for file acceptance. Routes
                every type to a dedicated handler.
        
        """
        typ_pfx = typ_pfx.decode().upper()

        if typ_pfx == 'M':
            # Standard message type.
            self._m_hndlr()
        elif typ_pfx == 'C':
            # For controller input.
            self._c_hndlr()
        elif typ_pfx == 'U':
            # User Found
            self._u_hndlr()
        elif typ_pfx == 'F':
            # For sending files.
            self._f_hndlr()
        elif typ_pfx == 'A':
            # Raises dialog for chosen recipient.
            self._a_hndlr()
        elif typ_pfx == 'X':
            # Transfer file.
            self._x_hndlr()
        else:
            print('-x- Unknown message type error.')

    def _m_hndlr(self):
        """Standard message. Unpacks message, and prints to own screen."""
        trim_msg = self.unpack_msg(serv_sock)
        self.print_message(trim_msg)

    def _c_hndlr(self):
        """Control messages from another user. Not displayed."""
        self.unpack_msg(serv_sock)

    def _u_hndlr(self):
        """Receives server response from user lookup. If False, rerun.
        
        After the server looks up a user, it sends its response as a U-type.
        The U type message either prompts the recipient if the exist, or asks
        the sender to re-enter their user choice.

        """

        # Reply from server.
        user_exists = self.unpack_msg(serv_sock).decode()

        if user_exists == "False":
            print("-!- They're not here. Try again. \n-=- Send to >> @", end='')
            self.message_type = 'U'

        elif user_exists == "True":
            # Prompt recipient.
            xfer.recip_prompt(serv_sock,
                              filename=self.path,
                              filesize=self.filesize)
            self.message_type = 'M'  # Reset message type.

    def _f_hndlr(self):
        """File Recipient. Prompts to accept or reject. Sends response."""

        # Display prompt sent from xfer.recip_prompt.
        recip_prompt = self.unpack_msg(serv_sock).decode()
        self.message_type = "A"
        print(recip_prompt)
        # Send answer as type A, user sends response back to server.

    def _a_hndlr(self):
        """Sender side. Answer from recipient. Y or N for filesend."""

        # Answer to prompt from F handler.
        recip_choice = self.unpack_msg(serv_sock).decode()

        # Resend if choice is nonsense.
        if recip_choice.lower() != 'y' and recip_choice.lower() != 'n':
            self.pack_n_send(serv_sock, 'F',
                             'Choice must be Y or N. Try again...')

        elif recip_choice.lower() == 'y':
            # Sender
            print("Sending file...")

            # Recipient
            xfer.file_xfer(serv_sock, self.path, self.filesize)
        elif recip_choice.lower() == 'n':
            self.pack_n_send(serv_sock, 'M', '-=- Transfer Cancelled.')

        self.message_type = 'M'

    def _x_hndlr(self):
        """File sender. Transfer handler."""
        XBFFR = 4086

        file_info = xfer.unpack_msg(serv_sock).decode()
        file_info = file_info.split('::')  # Arbitrary splitter.
        filesize = int(file_info[0])

        path = file_info[1]
        path = xfer.new_path(path)

        uneven_buffer = filesize % XBFFR

        print("-=- Receiving dawg!")

        chunk = serv_sock.recv(uneven_buffer)
        with open(path, 'wb') as f:
            f.write(chunk)

        bytes_recd = uneven_buffer  # start count

        while bytes_recd < filesize:
            chunk = serv_sock.recv(uneven_buffer)
            with open(path, 'ab') as f:
                f.write(chunk)
            bytes_recd += len(chunk)

        print(f"-=- {filesize}bytes received.")

    def start(self):
        self.t1 = Thread(target=self.receiver)
        self.t2 = Thread(target=self.sender)
        self.t1.start()
        self.t2.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Lightweight encrypted chat.',
                                     epilog='Going under...')

    parser.add_argument('-g',
                        '--goober',
                        help='Goober chat, or no encryption.',
                        action='store_false',
                        dest='is_encrypted')

    addr_group = parser.add_mutually_exclusive_group()

    addr_group.add_argument(
        '-f',
        '--full-address',
        help='Input full address. eg: xxx.xxx.xxx.xxx:######',
        action='store',
        type=str,
        dest='addr')
    addr_group.add_argument(
        '-H',
        '--host',
        help='Input host name or address. eg: xxx.xxx.xxx.xxx',
        action='store',
        type=str,
        dest='host')

    parser.add_argument('-P',
                        '--port',
                        help='Input port number.',
                        action='store',
                        type=int,
                        dest='port')

    args = parser.parse_args()

    if not args.addr:
        if not args.host:
            host = input('-+- Enter hostname of server: ')
            host = host or 'ubuntu'
        else:
            host = args.host
            print(f'-+- Hostname: {host}')

        if not args.port:
            port = input('-+- Choose port: ')
            port = port or '12222'
            port = int(port)
        else:
            port = args.port
            print(f'-+- Port: {port}')


    BFFR = 4096
    host = '127.0.0.1'
    # port = int(input('-=- Port, please: '))

    # DEBUG
    port = 1515

    xfer = FileXfer()
    channel = Client()

    serv_sock = socket.socket()
    serv_sock.connect((host, port))

    print(f'-+- Connected to {host}')
    # name = serv_sock.recv(BFFR)
    # print(name.decode())

    channel.start()
