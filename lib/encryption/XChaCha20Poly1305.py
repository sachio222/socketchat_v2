import os, json
from base64 import b64encode
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

# TODO: Add key writing...
import config.filepaths as paths

PATH = paths.chacha20_keys
FN = "chacha20.key"


def generate_key(path: str = PATH, fn: str = FN) -> bytes:
    """Generate and save keys."""
    key = get_random_bytes(32)
    with open(path + fn, 'wb') as f:
        f.write(key)
    return key


def load_key(path: str = PATH, fn: str = FN) -> bytes:
    try:
        with open(path + fn, 'rb') as f:
            key = f.read()
    except:
        print(
            f"[+] File not found at {path + fn}. \n[+] Generating new XChaCha20 key."
        )
        key = generate_key()

    return key

def write_key(key, path: str = PATH, fn: str = FN):
    with open(path + fn, 'wb') as f:
        f.write(key)


def load_key_for_xport(path: str = PATH, fn: str = FN) -> str:
    try:
        with open(path + fn, 'rb') as f:
            key = f.read()
    except:
        print(
            f"[+] File not found at {path + fn}. \n[+] Generating new XChaCha20 key."
        )
        key = generate_key()

    return b64encode(key).decode()


def encrypt(plaintext):
    plaintext = plaintext.encode()
    header = b'header'
    # plaintext = b'Half a league, Half a league...'
    key = load_key()
    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    cipher_text, tag = cipher.encrypt_and_digest(plaintext)

    jk = ['nonce', 'header', 'cipher_text', 'tag']
    jv = [
        b64encode(x).decode() for x in (cipher.nonce, header, cipher_text, tag)
    ]
    result = json.dumps(dict(zip(jk, jv)))
    # print(result)
    return result


# ===== DECODE

from base64 import b64decode
from Crypto.Cipher import ChaCha20_Poly1305


def decrypt(data):
    # Assume key was shared.
    plaintext = ""
    key = load_key()
    try:
        jk = ['nonce', 'header', 'cipher_text', 'tag']
        data = {k: b64decode(data[k]) for k in jk}
        cipher = ChaCha20_Poly1305.new(key=key, nonce=data["nonce"])
        cipher.update(data['header'])
        plaintext = cipher.decrypt_and_verify(data['cipher_text'], data['tag'])
        return plaintext

    except Exception as e:
        print(e)
        print('Incorrect decryption.')


def check_dir(self, path: str = PATH):
    if not os.path.exists(path):
        os.makedirs(path)


check_dir(PATH)
generate_key()

if __name__ == "__main__":
    msg = encrypt("hello")
    print(msg)
