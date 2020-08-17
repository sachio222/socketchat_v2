import nacl.utils
from nacl.public import PrivateKey, Box

# Generate Bob's private key.
seck_bob = PrivateKey.generate()

# Generate Bob's public key.
# Give to anyone who wants to send a msg to Bob.
pubk_bob = seck_bob.public_key

# Alice's private and public keys.
seck_alice = PrivateKey.generate()
# Give to anyone wanting to send a msg to her
pubk_alice = seck_alice.public_key

# Bob creates Box with his secret key and alice's pub k.
bob_box = Box(seck_bob, pubk_alice)

msg = b'What s that al about it is pretty fast!!'

# Encrypt the message, autogen nonce.
encrypted_msg = bob_box.encrypt(msg)

# or, pass it the nonce, which is not secret.
nonce = nacl.utils.random(Box.NONCE_SIZE)
encrypted_msg = bob_box.encrypt(msg, nonce)

print('nonce is:', nonce)
print('encrypted message is:', encrypted_msg)

# Decrypt the message.
alice_box = Box(seck_alice, pubk_bob)

# Decrypt message. An exception will be raised if encryption was tampered with.
# Or there was otherwise an error.
plaintext = alice_box.decrypt(encrypted_msg)
print(plaintext.decode())
