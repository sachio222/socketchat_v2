import nacl.utils
from nacl.public import PrivateKey, Box

class SaltCipher():

    def __init__(self):
        self.generate_keys()
        self.key = self.load_key()
        # self.f = Fernet(self.key)

    def generate_keys(self):
        self.set_pub_key(self.set_prv_key())
        
    def set_prv_key(self):
        _prv_key = PrivateKey.generate()
        with open('encryption/keys/nacl/prv.key', 'wb') as f:
            f.write(_prv_key)
        return _prv_key

    def set_pub_key(self, pvt_key):
        _pub_key = pvt_key.public_key
        with open('encryption/keys/nacl/pub.key', 'wb') as f:
            f.write(_pub_key)
        return _pub_key

    def make_public_box(self, my_prv, ur_pub):
        self.box = Box(my_prv, ur_pub)
        return self.box

    def encrypt(self, msg):
        cipher_msg = self.box.encrypt(msg)
        return cipher_msg

    def decrypt(self, msg):
        try:
            plaintext = self.box.decrypy(msg)
        except Exception:
            pass
        return plaintext

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
