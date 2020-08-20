import os
from cryptography.fernet import Fernet

key_path = 'encryption/keys/fernet/secret.key'


class FernetCipher():

    def __init__(self, path=key_path):
        self.key_path = path
        self._check_path(self.key_path)
        try:
            self.key = self.load_key()
        except:
            self.generate_key()
            self.key = self.load_key()

        self.f = Fernet(self.key)

    def generate_key(self):
        _key = Fernet.generate_key()
        with open(self.key_path, 'wb') as key_file:
            key_file.write(_key)

    def load_key(self):
        return open(self.key_path, 'rb').read()

    def encrypt(self, msg):
        msg = msg.encode()  # byte encode
        enc_msg = self.f.encrypt(msg)
        return enc_msg

    def decrypt(self, msg):
        try:
            dec_msg = self.f.decrypt(msg)
        except Exception:
            dec_msg = msg
        return dec_msg

    def split(self, raw_msg):
        """Separates message from raw_msg from server.

        Returns:
            handle: (str) user name
            cipher_msg: (bytes)
        """

        SEPARATOR = ': '
        _msg = raw_msg.decode()  # to str
        _split = _msg.split(SEPARATOR)
        handle = _split[0]
        cipher_msg = _split[1].encode()  # to bytes
        return handle, cipher_msg

    def _check_path(self, path):
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)
