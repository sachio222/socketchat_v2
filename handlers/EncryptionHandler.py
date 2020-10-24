import json
from chatutils import utils
from handlers.routers import EncryptionCmds

configs = utils.JSONLoader()

"""
# check config.
# I have been intrduced.
# Encryption is true.
# Get Encryption selection (AES256, XChaCha20Poly1305).
# Handle any size by passing through here.
# returns message as bytes.
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

def message_router(msg:str, *args, **kwargs) -> bytes:
    """Returns transmit buffer with message in proper encryption."""
    cipher_func = get_current_encryption()
    cipher_dict = cipher_func(msg)
    buffer = make_cipher_buffer(cipher_dict)
    return buffer

def pack_cipher_dict(cipher_text: bytes, *args, **kwargs) -> dict:
    """Pack ciphertext output into a dict."""
    enc_dict = {}
    enc_dict["cipher_text"] = cipher_text.decode()
    enc_dict = json.dumps(enc_dict)
    return enc_dict

def get_current_encryption(cipher:str = None) -> object:
    """Returns cipher from config list."""
    configs.reload() # Get current encryption setting.
    cipher = configs.dict["cipher"]
    cipher_func = EncryptionCmds.cipher_dict.get(cipher, "goober")
    return cipher_func

def make_cipher_buffer(cipher_dict:dict):
    """Returns transmit buffer with cipher type appended."""
    buffer = {}
    cipher_dict = json.loads(cipher_dict)
    buffer["cipher"] = configs.dict["cipher"]
    buffer["msg_pack"] = cipher_dict
    buffer = json.dumps(buffer)
    return buffer