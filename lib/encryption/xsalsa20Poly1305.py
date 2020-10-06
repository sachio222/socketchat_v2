import nacl.secret
import nacl.utils

key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

data = b"this is the message yo"

box = nacl.secret.SecretBox(key)
encrypted_msg = box.encrypt(data)

assert len(encrypted_msg) == len(data) + box.NONCE_SIZE + box.MACBYTES

plaintext = box.decrypt(encrypted_msg)

print(plaintext.decode('utf-8'))