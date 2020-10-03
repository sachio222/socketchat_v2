from chatutils import utils
from handlers.routers import EncryptionCmds

configs = utils.JSONLoader()

# aes = AES256Cipher()
# salt = NaclCipher()
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

def dispatch(msg:str, *args, **kwargs) -> bytes:
    buffer = {}
    configs.reload() # Get current encryption setting.
    cipher = configs.dict["cipher"]
    cipher = EncryptionCmds.cipher_dict.get(cipher, "goober")
    cipher_text = cipher(msg)

    # buffer["cipher"] = configs.dict["cipher"]
    # buffer["cipherText"] = cipher_text

    # print(buffer)

    return cipher_text