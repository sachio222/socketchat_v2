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

    def _rand_split(self, byt_str: bytes) -> (int, int, int):
        """Returns lengths of 2 rand. split bytes."""
        str_length = len(byt_str)
        seed = secrets.randbelow(str_length)
        split_a = str_length - seed
        split_b = str_length - split_a
        return split_a, split_b, str_length

    def pack_payload(self, msg: hex, nonce: hex) -> bytes:
        """Packs nonce with the ciphertext. Ready for sending. """
        nonce_b64 = codecs.encode(nonce, 'hex')
        ct_b64 = codecs.encode(msg, 'hex')
        a, b, b64_len = self._rand_split(nonce_b64)
        digits = a // 10 > 0
        count = int(digits) + 1
        payload = str(count).encode() + str(a).encode() + nonce_b64[:a] + ct_b64 + nonce_b64[-b:] + str(b64_len).encode()
        return payload

    def unpack_payload(self, payload : bytes) -> (hex, hex):
        """Unpacks the attached nonce and ciphertext."""
        payload = payload.decode()
        d = int(payload[0]); payload = payload[1:]
        a = int(payload[:d]); payload = payload[d:]
        l = int(payload[-2:]); payload = payload[:-2]
        b = l - a
        m = payload[a : -b]
        n = payload[:a] + payload[-b:]
        msg = codecs.decode(m.encode(), 'hex')
        nonce = codecs.decode(n.encode(), 'hex')
        return msg, nonce

    def _check_path(self, path):
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)

if __name__ == "__main__":
    aes = AES256Cipher()
    # Example usage:
    timea = time.perf_counter_ns()
    # Get message or file.
    msg = b"What is the question at hand? Do we evven really know?? What do we do if the message gets even huger? That's a big question to think about isn't it? Hmm but that's actually pretty cool, it is decrypting."
    # Pad it to AES block size.
    msg = aes.padder(msg, 128)
    # Encrypt message.
    msg, nonce = aes.encrypt(msg)
    # Pack payload if sending as bytestream.
    payload = aes.pack_payload(msg, nonce)    

    # Unpack payload of received bytes.
    msg, nonce = aes.unpack_payload(payload)
    # Decrypt message.
    msg = aes.decrypt(msg, nonce)
    # Remove padding from message.
    msg = aes.unpadder(msg)
    timeb = time.perf_counter_ns()
    print(msg)
    print('time:', (timeb-timea) / 1000000)
    

