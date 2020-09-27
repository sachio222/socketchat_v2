from chatutils import utils

from lib.encryption import XChaCha20Poly1305 
from lib.encryption.fernet import FernetCipher
from lib.encryption.salt import NaclCipher
from lib.encryption.aes256 import AES256Cipher

import nacl.utils
from nacl.encoding import Base64Encoder
from nacl.public import PublicKey, PrivateKey, Box

import config.filepaths as paths
configs = utils.JSONLoader()

aes = AES256Cipher()
salt = NaclCipher()
"""
check config.
I have been intrduced.
Encryption is true.
Get Encryption selection (AES256, ChaCha20Poly1305)
Handle any size by passing through here.
returns message as bytes.
"""
# class Encrypt():
#     def __init__(self, data):
#         configs.load()
#         self.encryption_method = cipher_dict.get(configs.cipher, goober)

#     def encryption_method(self, data) -> bytes:
#         """Returns encrypted bytes of passed in string, based on encrypt config."""

#         data_bytes = self.encryption_method(data)

#         return data_bytes

# if configs.introduced:
#     if self.encrypt_traffic:
#         self.msg = aes.full_encryption(self.msg.encode())
#         # print(self.msg)
# self.msg = aes.full_decryption(self.msg)

# print(self.msg)

# self.msg = nacl.encrypt(self.pub_box,
#                         self.msg.encode())
# self.msg = Base64Encoder.encode(self.msg)

# # self.msg = fernet.encrypt(self.msg)


def encrypt(msg):
    configs.load()
    encryption_method = cipher_dict.get(configs.cipher, goober)
    ciphertext = encryption_method(msg)
    return ciphertext


def encrypt_message(data):
    pass


def fernet(data) -> bytes:
    encrypted_msg = FernetCipher().encrypt(data)
    return encrypted_msg


def aes256_ctc(data):
    cipher_text = aes.full_encryption(data.encode())
    return cipher_text


def aes256_hmac(data):
    pass


def nacl_public_box(data):
    prv_key = salt.load_prv_key()
    pub_key = salt.load_pub_key()
    prv_key = PrivateKey(prv_key, encoder=Base64Encoder)
    pub_key = PublicKey(pub_key, encoder=Base64Encoder)
    box = salt.make_public_box(prv_key, pub_key)
    cipher_text = salt.encrypt(box, data.encode())
    cipher_text64 = Base64Encoder.encode(cipher_text)
    return cipher_text64



def nacl_secret_box(data):
    pass


def chacha20_poly1305(data):
    cipher_dict = XChaCha20Poly1305.encrypt(data)
    return cipher_dict


def argon(data):
    print("running argon dawg")


def goober(data) -> bytes:
    # print("Running naked dawg")
    return data.encode()


def test(data) -> bytes:
    encrypted_msg = f'<<{data}>>'
    return encrypted_msg.encode()


cipher_dict = {
    'fernet': fernet,
    'aes256': aes256_ctc,
    'aes256-hmac': aes256_hmac,
    'naclpub': nacl_public_box,
    'nacl-secret-box': nacl_secret_box,
    'chacha': chacha20_poly1305,
    'argon': argon,
    'goober': goober,
    'test': test
}
