#usr/bin python3

from tqdm import tqdm

# for i in tqdm(range(1000000000)):
#     pass
i=0 

while i < 10000000:
    with tqdm(total=10000000) as t:
        i += 1
        t.update(1)

# import os
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend

# backend = default_backend()
# key = os.urandom(32)
# iv = os.urandom(16)

# cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

# encryptor = cipher.encryptor()

# ct = encryptor.update(b"a secret message") + encryptor.finalize()
# print(ct)

# decryptor = cipher.decryptor()
# msg = decryptor.update(ct) + decryptor.finalize()

# print(msg)
