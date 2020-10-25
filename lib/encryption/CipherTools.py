import base64, json
from cryptography.hazmat.primitives.ciphers import AEADCipherContext

from nacl.public import Box, PrivateKey
from chatutils import utils

from lib.encryption import XChaCha20Poly1305
from lib.encryption.fernet import FernetCipher
from lib.encryption.salt import NaclCipher
from lib.encryption.aes256 import AES256Cipher

from nacl.encoding import Base64Encoder, HexEncoder, RawEncoder
from nacl.signing import SigningKey, VerifyKey

import config.filepaths as paths

public_box = None

def gen_nacl_keys(path=paths.nacl_keys, *args, **kwargs) -> tuple:
    """Generates public and private keys with nacl algorithm."""
    prvk, pubk = NaclCipher.generate_keys(path)
    prvk_b64 = prvk.encode(encoder=Base64Encoder)
    pubk_b64 = pubk.encode(encoder=Base64Encoder)
    
    return prvk_b64, pubk_b64

def gen_nacl_sign_keys(path=paths.nacl_keys, *args, **kwargs) -> tuple:
    sgnk, vfyk = NaclCipher.generate_signing_keys()
    sgnk_b64 = sgnk.encode(encoder=Base64Encoder)
    vfyk_b64 = vfyk.encode(encoder=Base64Encoder)
    
    return sgnk_b64, vfyk_b64

def pack_keys_for_xfer(pub_nacl_key: base64 = None,
                       prv_nacl_key: base64 = None,
                       path=paths.nacl_keys,
                       *args,
                       **kwargs) -> dict:

    key_pack = {}
    # prv_key = NaclCipher.load_prv_key() or prv_key
    public_box = make_nacl_pub_box(pub_nacl_key, prv_nacl_key)

    aes_key = AES256Cipher().load_key_for_xport()
    key_pack["aes"] = aes_key

    fernet_key = FernetCipher().load_key_for_xport()
    key_pack["fernet"] = fernet_key

    chacha_key = XChaCha20Poly1305.load_key_for_xport()
    key_pack["chacha"] = chacha_key

    key_pack = json.dumps(key_pack)

    enc_keys = public_box.encrypt(key_pack.encode())
    print("enc_keys are:", enc_keys)
    return enc_keys

def unpack_keys_from_xfer(key_pack_hex:hex, path=paths.nacl_keys,
                       *args,
                       **kwargs):

    global public_box

    try:
        key_dict = public_box.decrypt(key_pack_hex)
        print("key_dict is", key_dict)
    except:
        print("[!] Keys not unpacked. Try again.")


def make_nacl_pub_box(pub_key: base64 = None,
                      prv_key: base64 = None,
                      path=paths.nacl_keys,
                      *args,
                      **kwargs) -> Box:
    """Makes Nacl Public Box with mutual authentication."""
    
    global public_box

    prv_key = NaclCipher.load_prv_key() or prv_key
    public_box = NaclCipher.make_public_box(prv_key, pub_key)
    nacl_shrk = NaclCipher.gen_shared_key(public_box)
    
    print("-" * 60)
    print("Sharedkey", nacl_shrk)
    print("-" * 60)
    return public_box


# def NACL_DHKE(pub_key):
#     """Generate shared key from both keys."""
#     # Load my private_key
#     # Load their key.
#     # Make shared key.

#     return shared_key
