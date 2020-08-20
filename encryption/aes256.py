import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

key_path = 'encryption/keys/aes256/secret.key'

class AES256Cipher():
    def __init__(self):
        self.backend = default_backend()
        self.iv = secrets.token_bytes(16)
        self.key = self.generate_key()
        self.cipher = self.new_cipher(self.key, self.iv, self.backend)

    def generate_key(self):
        key = secrets.token_bytes(32)
        self._check_path(key_path)
        with open(key_path, 'wb') as key_file:
            key_file.write(key)

        return key

    def new_cipher(self, key, iv, backend):
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        return cipher

    def new_iv(self, iv) -> int:
        # iv = int(iv)
        # iv += 1
        # iv = hex(iv)
        return iv

    def padder(self, msg: bytes, size: int=128):
        padder = padding.ANSIX923(size).padder()
        padded_data = padder.update(msg)
        padded_data += padder.finalize()
        return padded_data

    def encrypt(self, msg: bytes) -> bytes:
        cipher = self.new_cipher(self.key, self.new_iv(self.iv), self.backend)
        self.iv = self.new_iv(self.iv)
        print('iv:', self.iv)
        encryptor = cipher.encryptor()
        cipher_txt = encryptor.update(msg) + encryptor.finalize()
        return cipher_txt

    def decrypt(self, cipher_txt: bytes) -> bytes:
        cipher = self.new_cipher(self.key, self.new_iv(self.iv), self.backend)
        decryptor = cipher.decryptor()
        msg = decryptor.update(cipher_txt) + decryptor.finalize()
        return msg

    def _check_path(self, path):
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)

if __name__ == "__main__":
    aes = AES256Cipher()
    print(aes.key)
    print(aes.iv)
    print(aes.cipher)
    msg = b'sup boo pp '
    msg = aes.padder(msg, 128)
    enc_msg = aes.encrypt(msg)
    print(enc_msg)

    pt = aes.decrypt(enc_msg)
    print(pt)
    msg = aes.padder(msg, 128)
    enc_msg = aes.encrypt(msg)
    print(enc_msg)
    pt = aes.decrypt(enc_msg)
    msg = aes.padder(msg, 128)
    enc_msg = aes.encrypt(msg)
    print(enc_msg)
    pt = aes.decrypt(enc_msg)
    msg = aes.padder(msg, 128)
    enc_msg = aes.encrypt(msg)
    print(enc_msg)
    pt = aes.decrypt(enc_msg)
    msg = aes.padder(msg, 128)
    enc_msg = aes.encrypt(msg)
    print(enc_msg)
    pt = aes.decrypt(enc_msg)

    

