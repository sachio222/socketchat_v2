import chatutils
from chatutils.chatio2 import ChatIO
from chatutils import utils
from handlers import EncryptionHandler

from lib.encryption import XChaCha20Poly1305, argon2kdf
from lib.encryption.fernet import FernetCipher
from lib.encryption.salt import NaclCipher
from lib.encryption.aes256 import AES256Cipher

import nacl.utils
from nacl.encoding import Base64Encoder
from nacl.public import PublicKey, PrivateKey, Box

configs = utils.JSONLoader()

aes = AES256Cipher()
salt = NaclCipher()
"""
#*****************************************************#
TO ADD CUSTOM ENCRYPTION:
    1. Add encryption/decrypton python fiile to filepath.
    2. Add command to cipher_dict
    3. Add method below. 
    
    Args: plaintext,
    Returns: bytes cipher_text(UTF-8)
"""


def fernet(data) -> bytes:
    """DECENT AES128 ENCRYPTION"""
    encrypted_msg = FernetCipher().encrypt(data)
    enc_dict = EncryptionHandler.pack_cipher_dict(encrypted_msg)
    return enc_dict


def aes256_ctc(data):
    """STATE OF THE ART AES256 ENCRYPTION"""
    encrypted_msg = aes.full_encryption(data.encode())
    encrypted_msg = EncryptionHandler.pack_cipher_dict(encrypted_msg)
    # print(cipher_text)
    return encrypted_msg


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
    """HIGH SPEED AUTHENTICATED ENCRYPTION"""
    cipher_dict = XChaCha20Poly1305.encrypt(data)
    return cipher_dict


def argon2(data):
    """ARGON2 PASSWORD HASHER."""
    hash, _ = argon2kdf.passwordHasher(data)
    print("Argon2 hash (random salt):", hash)
    enc_dict = EncryptionHandler.pack_cipher_dict(hash.encode())
    return enc_dict


def goober(data) -> bytes:
    """LIKE RUNNING IN THE BUFF"""
    encrypted_msg = EncryptionHandler.pack_cipher_dict(data.encode())
    return encrypted_msg


def test(data) -> bytes:
    data = f'<<{data}>>'
    encrypted_msg = EncryptionHandler.pack_cipher_dict(data.encode())
    return encrypted_msg


def xsalsa20(data) -> bytes:
    pass


cipher_dict = {
    'fernet': fernet,
    'aes256': aes256_ctc,
    'aes256-hmac': aes256_hmac,
    'naclpub': nacl_public_box,
    'nacl-secret-box': nacl_secret_box,
    'chacha': chacha20_poly1305,
    'argon2': argon2,
    'goober': goober,
    'test': test,
    'xsalsa20': xsalsa20
}
