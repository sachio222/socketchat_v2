import json
from base64 import b64encode
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes


def encrypt(plaintext):
    plaintext = plaintext.encode()
    header = b'header'
    # plaintext = b'Half a league, Half a league...'
    key = get_random_bytes(32)
    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    jk = ['nonce', 'header', 'ciphertext', 'tag']
    jv = [
        b64encode(x).decode() for x in (cipher.nonce, header, ciphertext, tag)
    ]
    result = json.dumps(dict(zip(jk, jv)))
    # print(result)
    return result


# ===== DECODE

from base64 import b64decode
from Crypto.Cipher import ChaCha20_Poly1305


def decrypt(result, key):
    # Assume key was shared.
    try:
        b64 = json.loads(result)
        jk = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in jk}
        cipher = ChaCha20_Poly1305.new(key=key, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        print(plaintext)

    except:
        print('Incorrect decryption.')


if __name__ == "__main__":
    msg = encrypt("hello")
    print(msg)
