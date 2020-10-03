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


def argon2(data):
    hash, _ = argon2kdf.passwordHasher(data)
    print("Argon2 hash (random salt):", hash)
    return hash.encode()


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
    'argon2': argon2,
    'goober': goober,
    'test': test
}
