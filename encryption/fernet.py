from cryptography.fernet import Fernet


class Cipher():

    def __init__(self):
        try:
            self.key = self.load_key()
        except:
            self.generate_key()
            self.key = self.load_key()

        self.f = Fernet(self.key)

    def generate_key(self):
        _key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(_key)

    def load_key(self):
        return open('secret.key', 'rb').read()

    def encrypt(self, msg):
        msg = msg.encode()  # byte encode
        enc_msg = self.f.encrypt(msg)
        return enc_msg

    def decrypt(self, msg):
        dec_msg = self.f.decrypt(msg)
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
