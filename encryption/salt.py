import nacl.utils
from nacl.public import PrivateKey, Box

class Cipher():
    
    def __init__(self):
        self.generate_keys()
        self.key = self.load_key()
        # self.f = Fernet(self.key)

    def generate_keys(self):
        _key = PrivateKey.generate()
        with open('/keys/saltsecret.key', 'wb') as key_file:
            key_file.write(_key)

    def get_pub_key(self):
        self.key

    def encrypt(self, msg):
        pass

    def decrypt(self, msg):
        try:
            pass
        except Exception:
            pass
        return msg

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
