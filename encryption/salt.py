import os
import nacl.utils
from nacl.public import PrivateKey, Box

class SaltCipher():
    def __init__(self):
        self.path = 'encryption/keys/nacl/'
        self.check_dir(self.path)
        my_prv, ur_pub = self.generate_keys()
        self.box = self.make_public_box(my_prv, ur_pub)

    def generate_keys(self):
        prv_key = PrivateKey.generate()
        pub_key = prv_key.public_key
        return prv_key, pub_key

    def make_public_box(self, my_prv, ur_pub):
        box = Box(my_prv, ur_pub)
        return box

    def encrypt(self, msg):
        cipher_msg = self.box.encrypt(msg.encode())
        return cipher_msg

    def decrypt(self, msg):
        # try:
        plaintext = self.box.decrypt(msg)
        # except Exception:
        #     plaintext = "Error, but I dunno what went wrong."
        #     print('Decrypytion error.')
        return plaintext.decode()

    def check_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

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

if __name__ == "__main__":
    salt = SaltCipher()

    msg = "hi how are you, this is my message"
    enc_msg = salt.encrypt(msg)
    dec_msg = salt.decrypt(enc_msg)
    print(msg)
    print(enc_msg)
    print(dec_msg)