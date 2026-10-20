from encryption.fernet import FernetCipher

if __name__ == "__main__":
    cipher = FernetCipher()
    cipher.generate_key()
    print(f'-+- New Fernet key saved to {cipher.key_path}')