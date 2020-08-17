import os
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder, RawEncoder, HexEncoder



class SaltCipher():

    def __init__(self):
        self.path = 'encryption/keys/nacl/'
        self.check_dir(self.path)
        self.my_prv, my_pub = self.generate_keys()
        # self.box = self.make_public_box(my_prv, ur_pub)

    def generate_keys(self):
        prv_key = PrivateKey.generate()
        self.pub_key = prv_key.public_key
        return prv_key, self.pub_key

    def get_pub_key(self):
        return self.pub_key

    def get_shared_key(self, ur_pub, filename='shared.key'):
        try:
            ur_pub = PublicKey(ur_pub, Base64Encoder)
        except: 
            print('Public key is invalid.')
            
        path = self.path + 'symm/'
        self.check_dir(path)

        box = self.make_public_box(ur_pub)

        self.sh_key = box.shared_key()

        print('running')
        with open(path + filename, 'wb') as f:
            f.write(self.sh_key)

        return self.sh_key

    def make_public_box(self, ur_pub):
        box = Box(self.my_prv, ur_pub)
        return box

    def encrypt(self, ur_pub, msg):
        self.box = self.make_public_box(ur_pub)
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
    a, b = salt.generate_keys()
    print('prv:', a)
    print('pub:', b)
    b_base = b.encode(Base64Encoder).decode()
    print('base64:', b_base)
    # b_raw = Base64Encoder.decode(b_base)
    b_raw = PublicKey(b_base, Base64Encoder)
    print('raw:', b_raw)
    print(b == b_raw)

    c = salt.get_shared_key(b)
    print(c)

    # d = '4gldSb3d54xRzz1XriLxbWMSxHEFqibqcxlvhKSsnmY='
    # print(Base64Encoder.decode(d))