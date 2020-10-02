import os
import sys
import socket

from .channel import Chime, Colors
from encryption.fernet import FernetCipher
from encryption.aes256 import AES256Cipher
from encryption.salt import NaclCipher, Box
from nacl.encoding import Base64Encoder

from chatutils import utils

configs = utils.JSONLoader()


class ChatIO(Chime, Colors):
    """Class for ChatIO"""

    def __init__(self, muted=False):
        super(ChatIO, self).__init__()
        self.aes = AES256Cipher()
        self.MAX_MSG_BYTES_LEN = configs.dict["system"]["maxMsgBytesLen"]
        self.muted = muted
        # Get color dicts
        self.style = self.set_style()
        self.bg = self.set_bg()
        self.txt = self.set_txt()

        self.GOLD_ULINE = self.format('ULINE', 'NONE', 'GOLD')
        self.GOLD_BOLD = self.format('BOLD', 'NONE', 'GOLD')
        self.GOLD = self.format('REG', 'NONE', 'GOLD')
        self.GREEN_ULINE = self.format('ULINE', 'BLACK', 'GREEN')
        self.GREEN_INVERT = self.format('INVERT', 'BLACK', 'GREEN')
        self.GREEN_BOLD = self.format('BOLD', 'BLACK', 'GREEN')
        self.GREEN = self.format('REG', 'BLACK', 'GREEN')
        self.BLUEGREY_ULINE = self.format('ULINE', 'GREY', 'BLUE')
        self.BLUEGREY_BOLD = self.format('BOLD', 'GREY', 'BLUE')
        self.BLACKGREY_BOLD = self.format('INVERT', 'GREY', 'BLACK')
        self.BLACKWHITE = self.format('INVERT', 'BLACK', 'WHITE')
        self.BLUEGREY = self.format('REG', 'GREY', 'BLUE')
        self.BLUEWHITE = self.format('INVERT', 'BLUE', 'GREY')
        self.GOLDBLACK_ULINE = self.format('ULINE', 'BLACK', 'GOLD')
        self.GOLDBLACK_BOLD = self.format('BOLD', 'BLACK', 'GOLD')
        self.GOLDBLACK = self.format('REG', 'BLACK', 'GOLD')

    def pack_n_send(self, sock, typ_pfx: str, msg: str):
        """Adds message type and message length to any message, and then sends.

        Converts any string to a prefixed bytes transmission that includes
        given message type prefix and a calculated length prefix. Receiving
        methods on SERVER and CLIENT both require this prefix and length for
        routing messages to their appropriate functions.
        
        typ_pfx: (Type prefix) 1 byte. tells recipient how to handle message. 
        len_pfx: (Length prefix) 4 bytes. tells socket when to stop receiving message.

        Args
            sock: (socket) Sending socket. Used with send method.
            typ_pfx: (str) A single char message type prefix read by the
                            recieving socket.
            msg: (str) Message that is sent.

        Example packet:
            b'M0005Hello' - Message type, 5 characters, "Hello"
            msg[0] - Message type
            msg[1:4] - Message length
            msg[5:] - Message
        """

        packed_msg = self.pack_message(typ_pfx, msg)
        sock.send(packed_msg.encode())

    def pack_message(self, typ_pfx, msg):
        """
        Example packet:
            b'M0005Hello' - Message type, 5 characters, "Hello"
            msg[0] - Message type
            msg[1:4] - Message length
            msg[5:] - Message
        """
        if type(typ_pfx) == bytes:
            typ_pfx = typ_pfx.decode()

        if type(msg) == bytes:
            msg = msg.decode()

        len_pfx = len(msg)
        len_pfx = str(len_pfx).rjust(self.MAX_MSG_BYTES_LEN, '0')
        packed_msg = f'{typ_pfx}{len_pfx}{msg}'

        return packed_msg

    def broadcast(self,
                  packed_msg,
                  all_sockets,
                  sender_socket,
                  target='other',
                  recip_socket=None,
                  sender=None):
        """
        uses
            all_sockets[sender_socket] to get SENDER address.
        """
        if type(packed_msg) != bytes:
            packed_msg = packed_msg.encode()

        if target == 'all':
            for sock in all_sockets:
                try:
                    sock.send(packed_msg)
                except:
                    pass
        elif target == 'self':
            for sock in all_sockets:
                if sock == sender_socket:
                    try:
                        sock.send(packed_msg)
                    except:
                        pass
        elif target == 'other':
            for sock in all_sockets:
                if sock != sender_socket:
                    try:
                        sock.send(packed_msg)
                    except:
                        pass
        elif target == 'recip':
            for sock in all_sockets:
                try:
                    if sock == recip_socket:
                        sock.send(packed_msg)
                except:
                    print('Provide valid recipient socket object.')
        elif not target:
            pass

        else:
            print(
                'Target type error: Must be "other", "self", "all", or "recip"')

    def unpack_msg(self, sock, shed_byte=False) -> bytes:
        """Unpacks prefix for file size, and returns trimmed message as bytes.
        
        This method does not read the message type. Call receiver() before
        invoking this method or else remove the first byte before reading with
        shed_byte=True. Once the input has been routed, this helper function is
        called to unpack the already sorted user inputs. 

        Args
            sock: (socket) Listening socket. Used with recv.
            shed_byte: (bool) Remove the 1st byte (type prefix)

        Returns
            trim_msg: (bytes) Message without prefixes.
        """

        if shed_byte:  # Removes type prefix
            sock.recv(1)

        sz_pfx = sock.recv(self.MAX_MSG_BYTES_LEN)
        buffer = self._pfxtoint(sock, sz_pfx, n=self.MAX_MSG_BYTES_LEN)
        trim_msg = sock.recv(buffer)

        return trim_msg  # As bytes

    def _pfxtoint(self, client_cnxn, data, n=4):
        """Converts size prefix data to int."""
        return int(data[:n])

    def print_message(self, msg, enc=False, style_name=None, box: Box = None):
        """Print message to screen."""

        ERASE_LINE = '\x1b[2K'
        sys.stdout.write(ERASE_LINE)

        if enc:
            try:
                # handle, msg = self.decrypt_incoming(msg,
                #                                     'nacl-pub-box',
                #                                     box=box)

                handle, msg = self.decrypt_incoming(msg,
                                                    encrpyt_method="aes256")

                handle = self.make_fancy(self.GREEN, f'@{handle}:')
                msg = self.make_fancy(self.GREEN, f' {msg}')
                print(f'\r{handle}{msg}')
            except:
                if type(msg) == bytes:
                    msg = msg.decode()

                self.play_chime()
                if style_name == "GREEN_INVERT":
                    msg = self.make_fancy(self.GREEN_INVERT, msg)

                elif style_name == "BLUEWHITE":
                    msg = self.make_fancy(self.BLACKWHITE, msg)

                else:
                    msg = self.make_fancy(self.BLACKGREY_BOLD, msg)
                print(f'\r{msg}')

        else:
            if type(msg) == bytes:
                msg = msg.decode()

            self.play_chime()
            if style_name == "GREEN_INVERT":
                msg = self.make_fancy(self.GREEN_INVERT, msg)

            elif style_name == "BLUEWHITE":
                msg = self.make_fancy(self.BLACKWHITE, msg)

            else:
                msg = self.make_fancy(self.BLACKGREY_BOLD, msg)

            print(f'\r{msg}')

    def remove_pfx(self, data, n=5):
        """UTILITY: cuts off the prefix for any reason."""
        # Accepts bytes input, chops off prefix and returns plain message as bytes.
        return data[5:]

    def split_to_str(self, raw_msg: bytes) -> tuple:
        """UTILITY: Separates message from raw_msg from server.

        Returns:
            handle: (str) user name
            cipher_msg: (bytes)
        """
        SEPARATOR = ': '
        msg = raw_msg.decode()  # to str
        split = msg.split(SEPARATOR)

        handle = split[0]
        cipher_msg = split[1]  # to bytes

        return handle, cipher_msg

    def _check_path(self, path):
        """UTILITY: Makes sure path exists."""
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)

    def decrypt_incoming(self,
                         raw_msg: bytes,
                         encrpyt_method: str = 'nacl-pub-box',
                         split: bool = True,
                         box: Box = None) -> tuple:

        if split:
            handle, msg = self.split_to_str(raw_msg)
            msg = msg.encode()  # To bytes
        else:
            handle = ''
            msg = raw_msg

        def dcryp_nacl_pub_box(msg: bytes, box) -> bytes:
            msg64 = Base64Encoder.decode(msg)
            dcrypt_msg = box.decrypt(msg64)
            return dcrypt_msg

        def dcryp_nacl_sld_box(msg: bytes, box) -> bytes:
            pass

        def dcryp_nacl_sec_box(msg: bytes, box) -> bytes:
            pass

        def dcryp_AES256(payload: bytes, *args) -> bytes:
            dcrypt_msg = self.aes.full_decryption(payload)
            return dcrypt_msg

        def dcryp_fernet(msg: bytes, *args) -> bytes:
            return FernetCipher().decrypt(msg).decode()

        def err_handler(*args) -> bytes:
            raise ValueError("encrypt_method must be 'nacl-pub-box', " \
                "'nacl-sld-box', 'nacl-sec-box', 'aes256', or 'fernet'")

        dispatch = {
            'nacl-pub-box': dcryp_nacl_pub_box,
            'nacl-sld-box': dcryp_nacl_sld_box,
            'nacl-sec-box': dcryp_nacl_sec_box,
            'aes256': dcryp_AES256,
            'fernet': dcryp_fernet
        }

        msg = dispatch.get(encrpyt_method, err_handler)(msg, box)
        msg = msg.decode()

        return handle, msg
