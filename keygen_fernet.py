from encryption.fernet import Cipher

if __name__ == "__main__":
    cipher = Cipher()
    cipher.generate_key()