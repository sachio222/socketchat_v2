from chatutils import utils

from lib.encryption import XChaCha20Poly1305
from lib.encryption.fernet import FernetCipher
from lib.encryption.salt import NaclCipher
from lib.encryption.aes256 import AES256Cipher

import config.filepaths as paths


def gen_nacl_key(path=paths.nacl_keys, *args, **kwargs):
    NaclCipher.generate_keys(path)
    print("[+] New NACL keys generated.")
