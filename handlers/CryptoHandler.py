"""
check config.
I have been intrduced.
Encryption is true.
Get Encryption selection (AES256, ChaCha20Poly1305)
Handle any size by passing through here.
returns message as bytes.
"""

def encrypt_message():
    pass
def fernet():
    pass
def aes256_ctc():
    pass
def aes256_hmac():
    pass
def nacl_public_box():
    pass
def nacl_secret_box():
    pass
def chacha20_poly1305():
    pass
def argon():
    pass

cipher_dict = {
    'fernet': fernet,
    'aes256-ctc': aes256_ctc,
    'aes256-hmac': aes256_hmac,
    'nacl-public-box': nacl_public_box,
    'nacl-secret-box': nacl_secret_box,
    'chacha20poly1305': chacha20_poly1305,
    'argon': argon,
}