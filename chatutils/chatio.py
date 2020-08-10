import os
import sys
import socket
from threading import Thread

from .channel import Chime
from encryption.fernet import Cipher


class ChatIO(Chime):
    """Class for ChatIO"""

    def __init__(self, muted=False):
        super(ChatIO, self).__init__()
        self.LEN_PFX_LEN = 4
        self.muted = muted

    def pack_n_send(self, sock, typ_pfx, msg):
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
        len_pfx = str(len_pfx).rjust(self.LEN_PFX_LEN, '0')
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
                sock.send(packed_msg)
        elif target == 'self':
            for sock in all_sockets:
                if sock == sender_socket:
                    sock.send(packed_msg)
        elif target == 'other':
            for sock in all_sockets:
                if sock != sender_socket:
                    sock.send(packed_msg)
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

    def unpack_msg(self, sock, shed_byte=False):
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

        sz_pfx = sock.recv(self.LEN_PFX_LEN)
        buffer = self._pfxtoint(sock, sz_pfx, n=self.LEN_PFX_LEN)
        trim_msg = sock.recv(buffer)

        return trim_msg  # As bytes

    def _pfxtoint(self, client_cnxn, data, n=4):
        """Converts size prefix data to int."""
        return int(data[:n])

    def print_message(self, msg, enc=False, style='yellow'):
        """Print message to screen.
        TODO
            add fun formatting.
            
        """

        if enc:
            handle, msg = self.split_n_decrypt(msg)
            print(f'\r{handle}: {msg.decode()}')

        else:
            if type(msg) == bytes:
                msg = msg.decode()

            ERASE_LINE = '\x1b[2K'
            sys.stdout.write(ERASE_LINE)

            self.play_chime()
            print(f'\r{msg}')

    def remove_pfx(self, data, n=5):
        # Accepts bytes input, chops off prefix and returns plain message as bytes.
        return data[5:]

    def split_n_decrypt(self, raw_msg):
        try:
            handle, msg = Cipher().split(raw_msg)
            msg = Cipher().decrypt(msg).decode()

        except:
            handle = None
            msg = raw_msg

        return handle, msg
