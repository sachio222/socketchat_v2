#!/usr/bin/ python3

import socket, ssl
import sys
from threading import Thread, Lock

import chatutils.xfer as xfer
import chatutils.utils as utils
from chatutils.chatio import ChatIO
from chatutils.channel import Channel

import encryption.x509 as x509

from handlers import ServMsgHandler
from lib.xfer.FileXfer import ServerOperations

configs = utils.JSONLoader()

# Global vars

# TODO: Are all these really necessary? Is there a better way?
sockets = {}  # socket : ip
sock_nick_dict = {}  # socket : nick
nick_addy_dict = {}  # nick : ip
user_key_dict = {}  # socket: key


class Server(ChatIO, Channel):
    """Server class"""

    def __init__(self):
        super(Server, self).__init__()
        # Init buffer, sender/recip socks
        self.BFFR = 1
        self.RECIP_SOCK = None
        self.SENDER_SOCK = None
        self.file_transfer = False

    def accept_connections(self):
        """Continuous Thread that listens for and accepts new socket cnxns."""

        # Accept connections.
        while True:
            client_cnxn, client_addr = sock.accept()
            # Wrap client connection in secure TLS wrapper.
            client_cnxn = server_ctxt.wrap_socket(client_cnxn, server_side=True)

            print(f'-+- Connected... to {client_addr}')
            sockets[client_cnxn] = client_addr  # Create cnxn:addr pairings.

            # Spin off thread for each client.
            Thread(target=self.handle_clients, args=(client_cnxn,)).start()

    def handle_clients(self, sock: socket):
        """Continuous thread, runs for each client that joins.
        
        Calls client_init, begins listening for message prefixes, and
        immediately routes them through the data_router. If data stops coming
        from a particular socket, it runs through clean up and removes all of
        their entries from the relevant dictionaries.
        """

        lock = Lock()

        # Init and welcome client.
        client_init = self.client_init(sock)

        # Start listening.
        while client_init:
            with lock:
                # Testing if with lock should work so msgs don't get
                #       separated from type prefix
                prefix_length = configs.dict["system"]["prefixLen"]
                data = sock.recv(prefix_length)

                # if not data:
                #     discon_msg = f'{sock_nick_dict[sock]} has been disconnected.'
                #     print(discon_msg)
                #     packed_msg = self.pack_message('S', discon_msg)
                #     self.broadcast(packed_msg, sockets, sock, 'other')

                #     # Clean up user artifacts
                #     if user_key_dict[sock]:
                #         del user_key_dict[sock]
                #     if (nick_addy_dict[sock_nick_dict[sock]]):
                #         del (nick_addy_dict[sock_nick_dict[sock]])
                #     if sock_nick_dict[sock]:
                #         del (sock_nick_dict[sock])
                #     if sockets[sock]:
                #         del (sockets[sock])  # remove address

                #     sock.close()
                #     break

                # self.data_router(sock, data)
                ServMsgHandler.data_router(sock, data)

    def data_router(self, client_cnxn, data):
        """Handles incoming data based on its message type."""
        # Send confirm dialog to recip if user is sending file.
        if data == "/".encode():
            # Drain socket of controller message so it doesn't print.
            control = self.unpack_msg(client_cnxn).decode()
            control = control.split(' ')

            if control[0] == 'status':
                # Send room status.
                # TODO: break into method.
                status, _ = self.get_status(nick_addy_dict)
                status = self.pack_message('S', status)
                if control[-1] == 'self':
                    target = 'self'
                else:
                    target = 'all'
                self.broadcast(status, sockets, client_cnxn, target=target)

        elif data == b'M':
            self._serv_m_handler(client_cnxn, data)
        elif data == b'U':
            self._serv_u_handler(client_cnxn)
        elif data == b'F':
            self._serv_f_handler(client_cnxn, data)
        elif data == b'A':
            self._serv_a_handler(client_cnxn, data)
        elif data == b'X':
            self._serv_x_handler(client_cnxn, data)
        elif data == b'x':
            self._serv_lil_x_handler(client_cnxn)
        elif data == b'P':
            # Pack public key.
            self._serv_p_handler(client_cnxn)
        elif data == b'T':
            # Trust user lookup.
            self._serv_t_handler(client_cnxn)
        elif data == b'V':
            self._serv_v_handler(client_cnxn)
        else:
            buff_text = self.unpack_msg(client_cnxn)
            data = self.pack_message(data, buff_text)
            self.broadcast(data, sockets, client_cnxn)

    #=== HANDLERS ===#
    def _serv_m_handler(self, sock: socket, data):
        """Standard message handler. Broadcast defaulted to 'other'."""

        sender = sock_nick_dict[sock]
        buff_text = self.unpack_msg(sock)
        buff_text = f'{sender}: {buff_text.decode()}'
        print(buff_text)
        data = self.pack_message(data, buff_text)
        self.broadcast(data, sockets, sock, sender=sender)

    def _serv_u_handler(self, sock: socket):
        """ U-type msgs used by SERVER and SENDER for user lookup exchanges.

        A U-type message tells the server to call lookup_user() method to
        search for a connected user by name. It sends the result back to
        SENDER.
        
        """
        username = self.unpack_msg(sock)
        if username != b'cancel':
            # Check for address.
            match = self.lookup_user(sock, username)
            # Send U type to sender.
            self.pack_n_send(sock, 'U', str(match))
        else:
            cancel_msg = 'x-x Send file cancelled. Continue chatting.'
            self.pack_n_send(sock, 'M', cancel_msg)

    def _serv_f_handler(self, sock, data):
        buff_text = self.unpack_msg(sock)
        data = self.pack_message(data, buff_text)
        self.broadcast(data,
                       sockets,
                       sock,
                       target='recip',
                       recip_socket=self.RECIP_SOCK)

    def _serv_a_handler(self, sock, data):
        buff_text = self.unpack_msg(sock)
        data = self.pack_message(data, buff_text)
        self.broadcast(data,
                       sockets,
                       sock,
                       target='recip',
                       recip_socket=self.SENDER_SOCK)

    def _serv_x_handler(self, client_cnxn, data):
        recd_bytes = 0
        buff_text = self.unpack_msg(client_cnxn)

        file_info = buff_text.decode().split('::')
        filesize = int(file_info[0])

        data = self.pack_message(data, buff_text)
        self.broadcast(data, sockets, client_cnxn, 'recip', self.RECIP_SOCK)

        while recd_bytes < filesize:
            chunk = client_cnxn.recv(4096)
            recd_bytes += len(chunk)
            self.broadcast(chunk, sockets, client_cnxn, 'recip',
                           self.RECIP_SOCK)

    def _serv_lil_x_handler(self, client_cnxn):
        # data = client_cnxn.recv(2048)
        # print('raw input data:', data)
        data = self.unpack_msg(client_cnxn)
        data = self.pack_message('x', data.decode())

        self.broadcast(data,
                       sockets,
                       client_cnxn,
                       target='recip',
                       recip_socket=self.RECIP_SOCK)
        # clear key data and sender/recip from server memory.
        del data
        del self.RECIP_SOCK
        del self.SENDER_SOCK

    def _serv_t_handler(self, client_cnxn):
        user_name = self.unpack_msg(client_cnxn)
        asker = sock_nick_dict[client_cnxn]
        user_found = self.lookup_user(client_cnxn, user_name)
        print('user found: ', user_found)
        if user_found:
            msg = f'@YO: Wanna trust @{asker} (Y/N)?'
            msg = self.pack_message('T', msg)
            self.broadcast(msg, sockets, client_cnxn, 'recip', self.RECIP_SOCK)

    def _serv_v_handler(self, client_cnxn):
        """Trust acquisition exchange."""
        choice = self.unpack_msg(client_cnxn).decode()

        if choice.lower() == 'y':
            a_key = user_key_dict[self.SENDER_SOCK]
            a_key = self.pack_message('k', a_key)  # small k
            b_key = user_key_dict[self.RECIP_SOCK]  # big K
            b_key = self.pack_message('K', b_key)

            msg = "Trust acquired. You are now chatting with some hardcore "\
                    "encryption."
            msg = self.pack_message('S', msg)
            # msg = "(If their text is green, it means you're good to go!!)"
            # msg = self.pack_message('M', msg)

            self.broadcast(a_key, sockets, client_cnxn, 'recip',
                           self.RECIP_SOCK)

            self.broadcast(b_key, sockets, client_cnxn, 'recip',
                           self.SENDER_SOCK)

            self.broadcast(msg, sockets, client_cnxn, 'recip', self.RECIP_SOCK)
            self.broadcast(msg, sockets, client_cnxn, 'recip', self.SENDER_SOCK)

        elif choice.lower() == 'n':
            msg = 'Trust not acquired.'
            msg = self.pack_message('S', msg)
            self.broadcast(msg, sockets, client_cnxn, 'recip', self.RECIP_SOCK)
            self.broadcast(msg, sockets, client_cnxn, 'recip', self.SENDER_SOCK)

    def _serv_p_handler(self, sock: socket):
        """Store public key on server on join."""
        # Stores public keys
        pubk64 = self.unpack_msg(sock)
        user_key_dict[sock] = pubk64

    def lookup_user(self, sock: socket, user_query: str) -> bool:
        """Checks if user exists. If so, returns user and address.

        Loops through the sock_nick_dict to check if the user is not the 
        user that is asking, and exists in the dict already.

        Args: 
            sock: (socket) Incoming socket object (from sender)
            user_query: (str) Name of user to look up.
        
        Returns
            match: (bool) True if user found
        """
        match = False
        # Stores sock of user being looked up.
        self.RECIP_SOCK = None
        # Stores sock of Who's askin?
        self.SENDER_SOCK = sock
        # If user_query happens to be bytes for some reason, decode it.
        try:
            user_query = user_query.decode()
        except:
            pass

        # Go through all the existing sockets/nicks
        for s, n in sock_nick_dict.items():
            if s != sock:  # Avoid self match.
                if n == user_query:
                    match = True
                    self.RECIP_SOCK = s
                    break
                else:
                    match = False

        return match

    def set_client_data(self, sock: socket) -> str:
        """Sets nick and addr of user."""

        unique = False
        PROMPT = 'Choose a handle:'
        # Asks user for handle as soon as they join the room.
        self.pack_n_send(sock, 'S', PROMPT)

        while not unique:
            # Receive input from user.
            user_name = self.unpack_msg(sock, shed_byte=True).decode()

            if not user_name:
                ERR = f"Handle needs at least one character. Try again."
                self.pack_n_send(sock, 'S', ERR)
                print(f'-x- {ERR}')  # Print to server.

            elif user_name not in sock_nick_dict.values():
                # If name does not exist, bag it, tag it.
                sock_nick_dict[sock] = user_name  # Create socket:nick pair.
                nick_addy_dict[user_name] = sockets[
                    sock]  # Create nick:addr pair.
                unique = True  # exit loop

            else:
                ERR = f"They're already here! Pick something else:"
                self.pack_n_send(sock, 'S', ERR)
                print(f'-x- {ERR}')  # Print to server.

        return user_name

    def client_welcome(self, sock: socket, user_name: str) -> bool:
        """Welcomes user and announces joining to rest. Returns bool.
        
        The Welcome message is sent as a 'W' type message which runs
        unique processes on the client side. It is always the very first
        message sent once a user has chosen a unique username, and is 
        therefore used as an initializing call to the client. Anything
        that should happen once, and only once on successful joining should
        be run under the W type message handler on the client side.
        
        Returns True when complete.
        """

        try:
            # TODO: put messages in dict.
            welcome_msg = "You're in. Welcome to the underground."
            announcement = f"@{user_name} is in the house!"

            # Sends 'W' Type message. Part of connection handshake.
            self.pack_n_send(sock, 'W', welcome_msg)
            # Broadcast to everyone that they're here.
            packed_msg = self.pack_message('S', announcement)
            self.broadcast(packed_msg, sockets, sock, target='other')
            # Announcement to server.
            print(f'-+- {announcement}')
            return True

        except Exception as e:
            print(f'-x- {e}')
            return False

    def client_init(self, sock: socket) -> bool:
        """Get unique username, welcome client to channel."""

        try:
            user_name = self.set_client_data(sock)
            self.client_welcome(sock, user_name)
            return True

        except Exception as e:
            print(f'-!- {e}')
            return False

    def start(self):
        """Begins the client acceptance loop as a threaded process."""
        Thread(target=self.accept_connections).start()


if __name__ == "__main__":
    MAX_CNXN = 5
    if sys.argv[-1] == 'debug':
        # Runs if last arg to server.py is 'debug'
        debug = True
    else:
        debug = False

    # TODO: Add inputs.
    x509 = x509.X509()
    server = Server()

    sock = socket.socket()
    host = socket.gethostname()

    if not debug:
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = socket.gethostbyname('localhost')

        print(f'-+- Starting server on host: {host}')
        print(f'-+- Host IP: {ip}')

        #-- use last cmd line arg as port #
        port = input(
            '-+- Choose port: ') if not sys.argv[-1].isdigit() else sys.argv[-1]
        if not port:
            port = 12222

        print(f'-+- Host Port: {port}')

        addy = (ip, int(port))
    else:
        # DEBUG for super quick server startup.
        addy = ('127.0.0.1', 12222)
        print(f'-!- Using debug parameters: {addy}')

    # TLS security is TLSv1.3, but is self signing for now.
    # All that is required for this, but will add CA later.
    rsa_key_path = 'encryption/keys/TLS/rsa_key.pem'
    cert_path = 'encryption/keys/TLS/certificate.pem'

    server_ctxt = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server_ctxt.verify_mode = ssl.CERT_NONE
    server_ctxt.set_ecdh_curve('prime256v1')
    server_ctxt.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384')
    server_ctxt.options |= ssl.OP_NO_COMPRESSION
    server_ctxt.options |= ssl.OP_SINGLE_ECDH_USE
    server_ctxt.options |= ssl.OP_CIPHER_SERVER_PREFERENCE
    server_ctxt.load_cert_chain(cert_path, rsa_key_path)

    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addy)

    except Exception as e:
        print(f'-x- {e}')
        utils.countdown(90)

    sock.settimeout(None)
    sock.listen(MAX_CNXN)

    print(f'-+- Waiting for secure connections...')
    server.start()
