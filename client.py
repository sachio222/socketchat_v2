#!/usr/bin/ python3
"""Encryptochat 2.0"""

import os
import sys
import socket, ssl
from threading import Thread
import argparse
import requests

from encryption.fernet import FernetCipher
from encryption.salt import NaclCipher
from encryption.aes256 import AES256Cipher

import nacl.utils
from nacl.encoding import Base64Encoder
from nacl.public import PublicKey, PrivateKey, Box

from chatutils import utils
from chatutils.xfer import FileXfer
from chatutils.chatio import ChatIO
from chatutils.channel import Chime

from handlers import InputHandler, EncryptionHandler


class Client(ChatIO):
    """
    Each message is prefixed with a single char, that helps it be sorted.
    """

    def __init__(self, muted=False):
        super(Client, self).__init__()
        self.muted = muted
        self.message_type = 'M'
        self.msg = None
        self.filesize = None
        self.path = None
        self.introduced = False
        self.encrypt_flag = True
        self.encrypt_traffic = self.encrypt_flag
        self.recip_pub_key = None
        self.pub_box = None
        self.sec_box = None

    #===================== SENDING METHODS =====================#
    def sender(self, sock):
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
            try:
                # Input
                msg = input('')

                data_bytes = InputHandler.input_router(sock, msg)

                if data_bytes:
                    # sock.send(data_bytes)
                    self.pack_n_send(sock, "M", data_bytes)

                # Check if controller message.
                # if self.msg:
                #     # If controller, skip to controller handler.
                #     if self.msg[0] == '/':
                #         typ_pfx = 'C'
                #         InputControl.input_command_handler(sock, self.msg)
                #         continue
                #     # Give it a prefix of self.message_type. Default is 'M'
                #     else:
                #         EncryptionControl.encryption_handler()
                # else:
                #     self.msg = ''

                # typ_pfx = self.message_type
                # self.pack_n_send(serv_sock, typ_pfx, self.msg)

            except Exception as e:
                print(e)
                serv_sock.close()
                exit()

            # !!!!! Always revert to default message_type and encryption.
            self.message_type = 'M'
            self.encrypt_traffic = self.encrypt_flag

    #===================== RECEIVING METHODS =====================#
    def receiver(self):
        """A Threaded socket that calls a function to check message type.
        
        A continuously running thread that listens for 1 byte of data. This
        one byte is responsible for routing all incoming signals from SERVER.
        Every incoming transmission is prefixed with a message type. If the
        prefix doesn't exist, it is considered a broken connection.

        The prefix is funneled into the Inbound Type Handler method or
        _inb_typ_handler, and is handled according to its type. 
        """

        while True:
            # Continually listen to first byte only.
            typ_pfx = serv_sock.recv(1)

            if not typ_pfx:
                serv_sock.close()
                print("-!- Aw, snap. Server's disconnected.")
                break

            # Send this byte downstream to the Inbound Type Handler.
            self._inb_typ_handler(serv_sock, typ_pfx)

        exit()

    #=================HANDLERS===================#

    def _m_handler(self, sock: socket):
        """Default. Prints to screen."""
        # shrk = nacl.gen_shared_key(self.pub_box)
        # print("Shared key # 2 is", shrk)
        trim_msg = self.unpack_msg(serv_sock)
        # print(trim_msg)
        # handle, msg = self.split_to_str(trim_msg)
        # # print(msg)
        # msg64 = Base64Encoder.decode(msg)
        # # print(msg64)
        # decrypted = self.pub_box.decrypt(msg64)
        # print(decrypted)
        self.print_message(trim_msg, enc=self.encrypt_traffic, box=self.pub_box)

    def _c_handler(self, sock: socket):
        """Incoming controller message."""
        self.unpack_msg(serv_sock)

    def _s_handler(self, sock: socket):
        """Server messages."""
        msg = self.unpack_msg(serv_sock).decode()
        msg = f"@YO: {msg}"
        self.print_message(msg, style_name='BLUEGREY')

    def _u_handler(self, sock: socket):
        """SERVER response regarding user.
        
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
                              path=self.path,
                              filename=self.filename,
                              filesize=self.filesize)
            self.message_type = 'M'  # Reset message type.
            self.encrypt_traffic = self.encrypt_flag  # Reset encryption

    def _f_handler(self, sock: socket):
        """Request from SENDER to confirm acceptance of file."""

        # Display prompt sent from xfer.recip_prompt.
        recip_prompt = self.unpack_msg(serv_sock).decode()

        self.message_type = "A"
        self.encrypt_traffic = False

        print(recip_prompt)
        # Send answer as type A, user sends response back to server.

    def _a_handler(self, sock: socket):
        """Response from RECIPIENT for confirmation of file acceptance."""

        # Answer to prompt from F handler.
        recip_choice = self.unpack_msg(serv_sock).decode()
        print('Sending...\r')

        # Resend if choice is nonsense.
        if recip_choice.lower() != 'y' and recip_choice.lower() != 'n':
            self.pack_n_send(serv_sock, 'F',
                             'Choice must be Y or N. Try again...')

        elif recip_choice.lower() == 'y':
            # Recipient
            xfer.file_xfer(serv_sock, self.path, self.filename, self.filesize)
            # Sender
            print("Sent...")

        elif recip_choice.lower() == 'n':
            self.pack_n_send(serv_sock, 'M', '-=- Transfer Cancelled.')

        self.message_type = 'M'

    def _x_handler(self, sock: socket):
        """Routes data from SENDER, passes thru SERVER, and stored by RECIPIENT."""
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
            print(f'{bytes_recd}/{filesize}\r', end='')
            chunk = serv_sock.recv(XBFFR)
            with open(path, 'ab') as f:
                f.write(chunk)
            bytes_recd += len(chunk)

        rec_msg = f"\r-=- {filesize}bytes received."
        print(rec_msg)

    def _lil_x_handler(self, sock: socket):
        """Write aes256 key to local file"""
        # print('running x handler')
        data = self.unpack_msg(sock)
        # print('enc_key:', data )
        data = Base64Encoder.decode(data)
        data = nacl.open_secret_box(self.secret_box, data)
        # print('aes256key:', data)
        if aes.write_key(data.encode()):
            print('-%- AES256 session key received.')

    def _w_handler(self, sock: socket):
        """Recv welcome msg. Send pub key."""
        msg = self.unpack_msg(serv_sock).decode()
        msg = f"-=- {msg}"
        self.print_message(msg, style_name='GREEN_INVERT')

        # Generate and upload public nacl key.
        _, my_pubk = nacl.generate_keys()
        my_pubk64 = nacl.encode_b64(my_pubk)
        self.pack_n_send(sock, 'P', my_pubk64)
        # print('my b64 public key:', my_pubk64)

        # self.introduced begins encryption after name has been sent.
        # this is because currently, the name is being sent/stored in plaintext.
        self.introduced = True
        self.pack_n_send(sock, '/', 'status self')

    def _t_handler(self, sock: socket):
        """Recv trust decision from askee."""
        # Answer to prompt from T handler.
        # Do you want to trust?
        wanna_trust_msg = self.unpack_msg(sock).decode()
        print(wanna_trust_msg)
        self.message_type = 'V'
        # Turn off encryption for answer.
        self.encrypt_traffic = False

    def _k_handler(self, sock: socket):
        """Recv. Keys"""
        pbk64 = self.unpack_msg(sock)
        # print('Their public key:', pbk64)
        recip_pbk = PublicKey(pbk64, Base64Encoder)
        print('-%- Public keys exchanged.')
        pvk64 = nacl.load_prv_key()
        pvk = PrivateKey(pvk64, encoder=Base64Encoder)
        self.pub_box = nacl.make_public_box(pvk, recip_pbk)
        # print(self.pub_box)
        shrk = nacl.gen_shared_key(self.pub_box)
        print('-%- Shared key generated.')
        # print("Shared key is", shrk)
        self.secret_box = nacl.make_secret_box(shrk)
        # print('Made secret box')
        aes_key = aes.generate_key()
        # print("I also made you an aes key:", aes_key)
        self.encrypt_flag = True
        self.encrypt_traffic = True
        aes_key = aes.hex_to_b64(aes_key)
        enc_key = nacl.put_in_secret_box(self.secret_box, aes_key)
        # print('encoded aes_key:', enc_key)
        enc_key = Base64Encoder.encode(enc_key)
        # print(enc_key)
        print('-%- AES256 session key shared.')
        self.pack_n_send(sock, 'x', enc_key)
        del aes_key

    def _lil_k_handler(self, sock: socket):
        pbk64 = self.unpack_msg(sock)
        recip_pbk = PublicKey(pbk64, Base64Encoder)
        print('-%- Public keys exchanged.')
        pvk64 = nacl.load_prv_key()
        pvk = PrivateKey(pvk64, encoder=Base64Encoder)
        self.pub_box = nacl.make_public_box(pvk, recip_pbk)
        # print(self.pub_box)
        shrk = nacl.gen_shared_key(self.pub_box)
        print('-%- Shared keys generated.')
        # print('Shared key is: ',shrk)
        self.secret_box = nacl.make_secret_box(shrk)
        # print('Made secret box')
        self.encrypt_flag = True
        self.encrypt_traffic = True

    def _err_handler(self, *args):
        # print('Prefix: ', typ_pfx)
        print('-x- Unknown message type error.')

    def _inb_typ_handler(self, sock: socket, typ_pfx: bytes):
        """Routes based on type.

        Incoming messages can be printed to the screen by default 'M', or be
        involved in a different flow, like receiving information from the
        SERVER about a the presence of a RECIPIENT in the chat.
        """

        try:
            typ_pfx = typ_pfx.decode()
            handler = self.dispatch_table.get(typ_pfx, self._err_handler)
            handler(self, sock)

        except:
            raise RuntimeError()

    dispatch_table = {
        'M': _m_handler,
        'C': _c_handler,
        'S': _s_handler,
        'U': _u_handler,
        'F': _f_handler,
        'A': _a_handler,
        'X': _x_handler,
        'x': _lil_x_handler,
        'W': _w_handler,
        'T': _t_handler,
        'K': _k_handler,
        'k': _lil_k_handler
    }

    def trust(self, msg):
        """TODO: Move to module."""
        #* Alices sends client lookup to server for 'Bob' with T(rust) type.
        #* Server listens for 'Trust' message. if receive:
        #* Server looks for bob in banks.
        #* IF server finds Bob, it broadcasts trust question and listens on V pipe.
        # if input to V pipe is Y, Server gets key by Alice and sends to bob as Key type
        # Server sends key to Bob with key type.
        # Keys are both shared and encryption is startd.
        user = ' '.join(msg[1:])
        while not user:
            user = input('Whom would you like to trust? @')
        self.pack_n_send(serv_sock, 'T', user)

    def start_sendfile_process(self, sock: socket):
        """A complex process that communicates between SERVER and 2 CLIENTS
        
        Steps to send a file with recipient and confirmation.

        1. CLIENT1: Wishes to send file.
        /sendfile -> sendfile_process...
        2. LOCAL CHANNEL: Asks for file to send.
        xfer.sender_prompt() -> bool
        3. LOCAL CHANNEL: Asks for recipient.
        xfer.user_prompt() -> xfer.get_username() -> sends U-type (user) message->
        4. SERVER: Receives U-type message.
        _serv_u_handler() -> lookup_user() -> sends bool as U-type reply to CLIENT1 ->
        5. CLIENT1: Receives U-type message.
        _u_handler() false ? -> U-type loop to SERVER | true ? xfer.recip_prompt(path, fn) -> CHANNEL
        6. LOCAL CHANNEL: Prints User Found, Sends fileinfo and accept prompt to CLIENT 2
        xfer.recip_prompt(path, fn) -> F-type (file) prompt - SERVER
        7. SERVER: Receives F-type message.
        _serv_f_handler() -> Prompt with file info as F-type msg -> CLIENT2
        8. CLIENT2: Prompt if wish to accept?
        _f_handler() -> Shows prompt, waits for answer as A-type (answer) -> 
        9. SERVER: Receives A-type message.
        _serv_a_handler() -> invalid? Loopback as F-type : valid? Routes A-type -> CLIENT1 as A-type msg ->
        10. CLIENT1: receives A-type message. Tells if accepted or rejected.
        _a_handler() -> 'n' ? break : 'y' ? xfer.file_xfer() -> Send as X-type (Xfer) -> SERVER
        11. SERVER: Receives X-type message.
        _serv_x_handler() -> transfers open buffer from CLIENT1 to CLIENT2
        12. CLIENT2: receives X-type message. File downloads
        x_handler() -> write file. -> print msg receipt as M-type (message). 
        Done.

        """

        self.path, self.filename, self.filesize = xfer.sender_prompt()
        if self.path:
            self.user = xfer.user_prompt(serv_sock)

    def sendkey(self, sock, msg):
        """1. LOCALCLIENT: Make sure the user is added. -> Y-type
        2. SERVER: Make sure user exists.
        3. LOCALCLIENT: Warn, this will share AES256 private key. sure?
        4. LOCALCLIENT: loadkey into var. pack it into sealed nacl box. Y-type.
        5. SERVER: Z-type. Push to RECIP. 
        6. CLIENT: Z-type. Store as key. 
        """
        print('printing getting username')
        user = xfer.get_username(sock)
        print(user)

    def start(self):
        self.t1 = Thread(target=self.receiver)
        self.t2 = Thread(target=self.sender, args=(serv_sock,))
        self.t1.start()
        self.t2.start()


if __name__ == "__main__":
    # Initialize paths to json parameters
    # # Load params json
    # assert json_path.is_file(
    # ), f"\n\nERROR: No config.json file found at {json_path}\n"

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

    # Establish keys
    fernet = FernetCipher()
    nacl = NaclCipher()
    aes = AES256Cipher()

    rsa_key_path = 'encryption/keys/TLS/rsa_key.pem'
    cert_path = 'encryption/keys/TLS/certificate.pem'

    client_ctxt = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    client_ctxt.check_hostname = False
    client_ctxt.verify_mode = ssl.CERT_NONE
    client_ctxt.set_ciphers('ECDHE-ECDSA-AES256-SHA384')
    client_ctxt.options |= ssl.OP_NO_COMPRESSION
    client_ctxt.load_verify_locations(cert_path)

    # If you want to lock with cert password.
    # client_ctxt.load_cert_chain(cert_path, rsa_key_path)

    serv_sock = socket.socket()

    # Create SSL sock.
    serv_sock.connect((host, port))
    serv_sock = client_ctxt.wrap_socket(serv_sock, server_hostname=host)

    print(f'-+- SSL Established. {serv_sock.version()}')
    print(f'-+- Connected to {host}')
    # print(f'Peer certificate: {serv_sock.getpeercert()}')
    # print(f'Ciphers: {client_ctxt.get_ciphers()}')

    # Lock to false for now.
    args.is_encrypted = False

    channel.encrypt_flag = args.is_encrypted
    if channel.encrypt_flag:
        encr_msg = f'\n-!- 🔐 Encryption is ON.\n-!- However, your handle may still be visible in plaintext.'
    else:
        encr_msg = f'-!- 🔓 Encryption is OFF.'

    channel.print_message(encr_msg, style_name='BLUEWHITE')
    channel.start()
