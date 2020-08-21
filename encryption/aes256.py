import os
import secrets
import codecs
import time

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

key_path = 'encryption/keys/aes256/secret.key'


class AES256Cipher():

    def __init__(self):
        self.backend = default_backend()
        self.iv = self.new_iv()
        self.key = self.generate_key()
        self.cipher = self.new_cipher(self.key, self.iv, self.backend)
        self.nonce = None
        self.IVb = 16

    def generate_key(self):
        key = secrets.token_bytes(32)
        self._check_path(key_path)
        with open(key_path, 'wb') as key_file:
            key_file.write(key)

        return key

    def new_cipher(self, key, iv, backend):
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        return cipher

    def new_iv(self) -> int:
        iv = secrets.token_bytes(16)
        return iv

    def padder(self, msg: bytes, nonce: bytes, size: int = 128) -> bytes:
        padder = padding.ANSIX923(size).padder()
        padded_data = padder.update(msg)
        padded_data += padder.finalize()
        return padded_data

    def unpadder(self, padded_data: bytes, size: int = 128) -> bytes:
        unpadder = padding.ANSIX923(128).unpadder()
        data = unpadder.update(padded_data)
        data = data + unpadder.finalize()
        return data

    def encrypt(self, msg: bytes) -> bytes:
        self.nonce = self.new_iv()
        # print('The nonce:', self.nonce)
        cipher = self.new_cipher(self.key, self.nonce, self.backend)
        encryptor = cipher.encryptor()
        cipher_txt = encryptor.update(msg) + encryptor.finalize()
        return cipher_txt, self.nonce

    def decrypt(self, cipher_txt: bytes, nonce: bytes) -> bytes:
        cipher = self.new_cipher(self.key, nonce, self.backend)
        decryptor = cipher.decryptor()
        msg = decryptor.update(cipher_txt) + decryptor.finalize()
        return msg

    def _check_path(self, path):
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)


if __name__ == "__main__":
    aes = AES256Cipher()
    msg = b"What is the question at hand? Do we evven really know?? What do we do if the message gets even huger? That's a big question to think about isn't it? Hmm but that's actually pretty cool, it is decrypting."
    timea = time.perf_counter_ns()
    msg = aes.padder(msg, 128)
    msg, nonce = aes.encrypt(msg)

    b64n = codecs.encode(nonce, 'hex')
    b64_pkt = codecs.encode(msg, 'hex')

    def _rand_split(byt_str: bytes) -> (int, int, int):
        """Returns lengths of 2 rand. split bytes."""
        str_length = len(byt_str)
        seed = secrets.randbelow(str_length)
        split_a = str_length - seed
        split_b = str_length - split_a
        return split_a, split_b, str_length

    def pack_payload(nonce_b64, ct_b64) -> bytes:
        """Packs nonce with the ciphertext. Ready for sending. """
        a, b, b64_len = _rand_split(nonce_b64)
        digits = a // 10 > 0
        count = int(digits) + 1
        payload = str(count).encode() + str(a).encode() + nonce_b64[:a] + ct_b64 + nonce_b64[-b:] + str(b64_len).encode()
        return payload

    def unpack_payload(payload):
        """Unpacks the attached nonce and ciphertext."""
        payload = payload.decode()
        d = int(payload[0]); payload = payload[1:]
        a = int(payload[:d]); payload = payload[d:]
        l = int(payload[-2:]); payload = payload[:-2]
        b = l - a
        m = payload[a : -b]
        n = payload[:a] + payload[-b:]
        return m.encode(), n.encode()


    payload = pack_payload(b64n, b64_pkt)    

    msg, nonce = unpack_payload(payload)
    msg = codecs.decode(msg, 'hex')
    nonce = codecs.decode(nonce, 'hex')

    msg = aes.decrypt(msg, nonce)
    msg = aes.unpadder(msg)
    timeb = time.perf_counter_ns()
    print('time:', (timeb-timea) / 1000000)

    print(msg)

