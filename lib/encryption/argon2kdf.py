# Argon2.
"""Modern, ASIC resistent, GPU resistent, better password cracking resistance than
    all of em. 

https://pypi.org/project/argon2-cffi/
    
variations:
    Argon2d - strong GPU resistence, but side channel attacks. 
    Argon2i - less gpu resistance, no side channel attacks. 
    Argon2id - Recommended, combines argon2d and argon 2i (argonautica)

params:
    password P: the password (or message) to be hashed
    salt S: random-generated salt (16 bytes recommended for password hashing)
    iterations t: number of iterations to perform
    memorySizeKB m: amount of memory (in kilobytes) to use
    parallelism p: degree of parallelism (i.e. number of threads)
    outputKeyLength T: desired number of returned bytes

When to use:
    When configured properly Argon2 is considered a highly secure KDF function,
    one of the best available in the industry, so you can use it as general
    purpose password to key derivation algorithm, e.g. to when encrypting
    wallets, documents, files or app passwords. In the general case Argon2 is
    recommended over Scrypt, Bcrypt and PBKDF2.
"""

import argon2, binascii


def raw_hash_with_salt(password: str = 'pw1234', salt: str = 'custom salt'):
    password = password.encode()
    salt = salt.encode()
    hash = argon2.hash_password_raw(time_cost=16,
                                    memory_cost=2**15,
                                    parallelism=2,
                                    hash_len=32,
                                    password=password,
                                    salt=salt,
                                    type=argon2.low_level.Type.ID)

    print('Argon2 raw hash:', binascii.hexlify(hash))


def passwordHasher(password: str = "pw1234", write=False):
    argon2Hasher = argon2.PasswordHasher(time_cost=16,
                                         memory_cost=2**15,
                                         parallelism=2,
                                         hash_len=32,
                                         salt_len=16)
    hash = argon2Hasher.hash(password)
    # print("Argon2 hash (random salt):", hash)

    # print(dir(argon2Hasher))

    verifyValid = argon2Hasher.verify(hash, password)
    # print('Argon2 verify (correct password):', verifyValid)

    # try:
    #     argon2Hasher.verify(hash, 'wrong123')
    # except:
    #     print("Argon2 verify (incorrect password):", False)

    return hash, argon2Hasher
