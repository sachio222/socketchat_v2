from chatutils import utils

from lib.encryption import XChaCha20Poly1305
from lib.encryption.fernet import FernetCipher
from lib.encryption.salt import NaclCipher
from lib.encryption.aes256 import AES256Cipher

from nacl.encoding import Base64Encoder, HexEncoder, RawEncoder


import config.filepaths as paths


def gen_nacl_key(path=paths.nacl_keys, *args, **kwargs) -> tuple:
    prvk, pubk = NaclCipher.generate_keys(path)
    prvk_b64 = prvk.encode(encoder=Base64Encoder)
    pubk_b64 = pubk.encode(encoder=Base64Encoder)
    print("[+] New NACL keys generated.")
    return prvk_b64, pubk_b64
