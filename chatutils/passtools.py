import argon2

from chatutils import utils
import config.filepaths as paths

hash_json = utils.JSONLoader(paths.hashes)


def password_verify(which_hash: str, password: str) -> bool:
    hash = getattr(hash_json, which_hash)
    ph = argon2.PasswordHasher(time_cost=16,
                               memory_cost=2**15,
                               parallelism=2,
                               hash_len=32,
                               salt_len=16)
    try:
        verification = ph.verify(hash, password)
    except Exception as e:
        print(e)
        verification = False

    return verification


def request_password(which_hash):
    pw = input("[+] Input current password: ")
    match = password_verify(which_hash, pw)
    return match


def set_password(which_hash):
    ph = argon2.PasswordHasher(time_cost=16,
                               memory_cost=2**15,
                               parallelism=2,
                               hash_len=32,
                               salt_len=16)

    new_pw = input("[+] Input new password: ")
    new_pw2 = input("[+] Confirm new password: ")

    if new_pw == new_pw2:
        hash = ph.hash(new_pw)
        setattr(hash_json, which_hash, hash)
        hash_json.update(paths.hashes)
        print("[+] Password updated!")
    else:
        print("[!] Passwords don't match. Try again.")
        hash = None
    return hash


def request_password_reset(which_hash):
    print("[+] Reset password")
    match = request_password(which_hash)
    if match:
        set_password(which_hash)
    return


# request_password_reset("admin")
# password_verify("admin", "pass")
