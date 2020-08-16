#!/usr/bin/ python3
"""Encryptochat 2.0"""

import os
import sys
import socket, ssl
from threading import Thread
import argparse
import requests

from encryption.fernet import Cipher

from chatutils import utils
from chatutils.xfer import FileXfer
from chatutils.chatio import ChatIO
from chatutils.channel import Chime

from addons import weather, urbandict, moon


class Client(ChatIO):
    """
    Each message is prefixed with a single char, that helps it be sorted.
    """

    def __init__(self, muted=False):
        super(Client, self).__init__()
        self.muted = muted
        self.message_type = 'M'
        self.msg = ''
        self.filesize = ''
        self.path = ''
        self.introduced = False
        self.encrypt_flag = True
        self.encrypt_traffic = self.encrypt_flag

    #===================== SENDING METHODS =====================#
    def sender(self):
        """Accepts user input, checks type, and begins sending to recip.

        The sender function is a continuously running input thread. Any time
        a user presses enter on the UI, it goes through this function. It can
        get in the way and be tricky sometimes, so it needs to be handled
        thoughtfully. The default prefix is 'M' for message.

        One way of managing flow is by modifying self.message_type. Inputs
        are routed through the app based on their first character, known as the
        message type, or type prefix (typ_prefix). Based on this prefix, the 
        input can be routed anywhere in the app.

        """

        while True:

            # Input
            self.msg = input('')

            # Check for controller message.
            if self.msg:
                # If controller, skip to controller handler.
                if self.msg[0] == '/':
                    typ_pfx = 'C'
                    self.inp_ctrl_handler(self.msg)
                    continue

                # Give it a prefix of self.message_type. Default is 'M'
                else:
                    # If name has been given, encrypt everything else.
                    if self.introduced:
                        if self.encrypt_traffic:
                            self.msg = cipher.encrypt(self.msg)

                # typ_pfx = self.message_type
                # self.pack_n_send(serv_sock, typ_pfx, self.msg)

            else:
                self.msg = ''
                # pass

            typ_pfx = self.message_type
            self.pack_n_send(serv_sock, typ_pfx, self.msg)

            # Always revert to default message_type and encryption.
            self.message_type = 'M'
            self.encrypt_traffic = self.encrypt_flag

    def inp_ctrl_handler(self, msg):
        """Sorts through input control messages and calls controller funcs.
        
    
        All of the controller commands are routed through this function based
        on the presence of a "/" character at the beginning of the command,
        which is detected by the sender function. Each command has a different
        end point and they all behave differently depending on their defined
        purposes.

        Args
            msg - (Usually str) - the raw input command before processing.
        """

        if type(msg) == bytes:
            msg.decode()

        if msg == '/about':
            # Read from file in config folder.
            path = 'config/about.txt'
            utils.print_from_file(path)

        elif msg == '/help' or msg == '/h':
            # Read from file in config folder.
            path = 'config/help.txt'
            utils.print_from_file(path)

        elif msg == '/sendfile' or msg == '/sf':
            # Initiates Send File (SF) sequence.
            # /SF1: Confirm file is available.
            self.path, self.filesize = xfer.sender_prompt()

            # /SF2: Check that RECIPIENT exists.
            if self.path:
                self.user = xfer.user_prompt(serv_sock)

        elif msg[:7] == '/status':
            # Ask SERVER to broadcast who is online.
            msg = msg[1:]
            self.pack_n_send(serv_sock, '/', msg)
        
        elif msg == '/mute':
            self.muted = True
            self.print_message("@YO: Muted. Type /unmute to restore sound.")

        elif msg == '/unmute':
            self.muted = False
            self.print_message("@YO: B00P! Type /mute to turn off sound.")

        elif msg == '/exit' or msg == '/close':
            print('Disconnected.')
            serv_sock.shutdown(socket.SHUT_RDWR)
            serv_sock.close()
            pass

        elif msg[:8] == '/weather':
            weather.report(msg)
            # print('\r-=-', report)
        
        elif msg[:7] == '/urband':
            urbandict.urbandict(msg)

        elif msg == '/moon':
            moon.phase()

        else:
            print('-!- Command not recognized.')

    #===================== RECEIVING METHODS =====================#
    def receiver(self):
        """A Threaded socket that calls a function to check message type.
        
        A continuously running thread that listens for 1 byte of data. This
        one byte is responsible for routing all incoming signals from SERVER.
        Every incoming transmission is prefixed with a message type. If the
        prefix doesn't exist, it is considered a broken connection.

        The prefix is funneled into the Inbound Type Handler method or
        _inb_typ_hndlr, and is handled according to its type. 
        """

        while True:
            # Continually listen to first byte only.
            typ_pfx = serv_sock.recv(1)

            if not typ_pfx:
                serv_sock.close()
                print("-!- Aw, snap. Server's disconnected.")
                break

            # Send this byte downstream to the Inbound Type Handler.
            self._inb_typ_hndlr(typ_pfx)

        exit()

    def _inb_typ_hndlr(self, typ_pfx):
        """Routes incoming messages based on message type. Default is 'M'.

        Incoming messages can be printed to the screen by default, or be
        involved in a different flow, like receiving information from the
        SERVER about a the presence of a RECIPIENT in the chat.

        The Inbound Type Handler routes each message to a downstream handler
        methods designed for each function. Those handlers are each unique
        and are based on the requirements of that message type.
        """
        try:
            typ_pfx = typ_pfx.decode().upper()

            if typ_pfx == 'M':
                # Default. Prints to screen.
                self._m_hndlr()
            elif typ_pfx == 'C':
                # Incoming controller message.
                self._c_hndlr()
            elif typ_pfx == 'S':
                # Server messages.
                self._s_hndlr()
            elif typ_pfx == 'U':
                # SERVER response regarding user.
                self._u_hndlr()
            elif typ_pfx == 'F':
                # Request from SENDER to confirm acceptance of file.
                self._f_hndlr()
            elif typ_pfx == 'A':
                # Response from RECIPIENT for confirmation of file acceptance.
                self._a_hndlr()
            elif typ_pfx == 'X':
                # Routes data from SENDER, passes thru SERVER, and stored by RECIPIENT.
                self._x_hndlr()
            elif typ_pfx == 'W':
                self._w_hndlr()
            else:
                print('Prefix: ', typ_pfx)
                print('-x- Unknown message type error.')
        except:
            pass

    def _m_hndlr(self):
        """Standard message. Unpacks message, and prints screen."""
        trim_msg = self.unpack_msg(serv_sock)
        self.print_message(trim_msg, enc=self.encrypt_traffic)

    def _c_hndlr(self):
        """Control messages from another user. Not displayed."""
        self.unpack_msg(serv_sock)

    def _s_hndlr(self):
        """Server announcements."""
        msg = self.unpack_msg(serv_sock).decode()
        msg = f"@YO: {msg}"
        self.print_message(msg, style_name='BLUEGREY')

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
            self.encrypt_traffic = False

        elif user_exists == "True":
            # Prompt recipient.
            xfer.recip_prompt(serv_sock,
                              filename=self.path,
                              filesize=self.filesize)
            self.message_type = 'M'  # Reset message type.
            self.encrypt_traffic = self.encrypt_flag  # Reset encryption

    def _f_hndlr(self):
        """File Recipient. Prompts to accept or reject. Sends response."""

        # Display prompt sent from xfer.recip_prompt.
        recip_prompt = self.unpack_msg(serv_sock).decode()

        self.message_type = "A"
        self.encrypt_traffic = False

        print(recip_prompt)
        # Send answer as type A, user sends response back to server.

    def _a_hndlr(self):
        """Sender side. Answer from recipient. Y or N for filesend."""

        # Answer to prompt from F handler.
        recip_choice = self.unpack_msg(serv_sock).decode()
        print('Sending...\r')

        # Resend if choice is nonsense.
        if recip_choice.lower() != 'y' and recip_choice.lower() != 'n':
            self.pack_n_send(serv_sock, 'F',
                             'Choice must be Y or N. Try again...')

        elif recip_choice.lower() == 'y':
            # Sender
            print("Sent...")

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
            chunk = serv_sock.recv(XBFFR)
            with open(path, 'ab') as f:
                f.write(chunk)
            bytes_recd += len(chunk)

        rec_msg = f"-=- {filesize}bytes received."
        print(rec_msg)

    def _w_hndlr(self):
        """Welcome method."""
        msg = self.unpack_msg(serv_sock).decode()
        msg = f"-=- {msg}"
        self.print_message(msg, style_name='GREEN_INVERT')
        self.introduced = True
        self.pack_n_send(serv_sock, '/', 'status self')

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
    # host = '192.168.68.143'
    # port = int(input('-=- Port, please: '))

    # # DEBUG
    # port = 1515

    xfer = FileXfer()
    channel = Client()
    cipher = Cipher()

    rsa_key_path = 'encryption/keys/TLS/rsa_key.pem'
    cert_path = 'encryption/keys/TLS/certificate.pem'
    

    client_ctxt = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    client_ctxt.check_hostname = False
    # client_ctxt.verify_mode = ssl.CERT_REQUIRED
    client_ctxt.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
    client_ctxt.options |= ssl.OP_NO_COMPRESSION
    client_ctxt.load_cert_chain(cert_path, rsa_key_path)

    serv_sock = socket.socket()
    
    # Create SSL sock.
    serv_sock.connect((host, port))
    serv_sock = client_ctxt.wrap_socket(serv_sock, server_hostname=host)

    print(f'-+- SSL Established. {serv_sock.version()}')
    print(f'-+- Connected to {host}')
    # print(f'Peer certificate: {serv_sock.getpeercert()}')

    channel.encrypt_flag = args.is_encrypted
    if channel.encrypt_flag:
        encr_msg = f'\n-!- 🔐 Encryption is ON.\n-!- However, your handle may still be visible in plaintext.'
    else:
        encr_msg = f'-!- 🔓 Encryption is OFF.'

    channel.print_message(encr_msg, style_name='BLUEWHITE')
    channel.start()
