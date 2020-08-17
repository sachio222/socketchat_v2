import os
import nacl.utils
from nacl.secret import SecretBox
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder, HexEncoder
from nacl.signing import SigningKey, SignedMessage, VerifyKey

class SaltCipher():
    """Based on the python fork of nacl's libsodium framework.
    
    The salt cipher involves state of the art encryption for assymetric
    encryption between users with the exchange of public keys and the
    creation of a shared secret. Also allows for signing/verification.
    """

    def __init__(self, path: str = 'encryption/keys/nacl/'):
        self.path = path
        self.check_dir(self.path)
        self.prv_key, self.pub_key = self.generate_keys()

    def generate_keys(self,
                      prv_fn: str = 'private.key',
                      pub_fn: str = 'public.key') -> (PrivateKey, PublicKey):
        """Generate and save key pair. Use HexEncoder to write to bytes."""

        # Generate a private key.
        prv_key = PrivateKey.generate()
        with open(self.path + prv_fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(prv_key.encode(encoder=Base64Encoder))

        # Get public key from private.
        pub_key = prv_key.public_key
        with open(self.path + pub_fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(pub_key.encode(encoder=Base64Encoder))

        return prv_key, pub_key

    def load_pub_key(self, fn: str = 'public.key') -> PublicKey:
        """Returns PublicKey as Base64. Use encoder=Base64Encoder for bytes."""

        pub_key = None
        try:
            with open(self.path + fn, 'rb') as f:
                pub_key = f.read()
        except FileNotFoundError:
            print(f"File not found at {self.path + fn}. Try again.")
        return pub_key

    def load_prv_key(self, fn: str = 'private.key') -> PrivateKey:
        """Returns PrivateKey as Base64. Use encoder=Base64Encoder for bytes."""

        prv_key = None
        try:
            with open(self.path + fn, 'rb') as f:
                prv_key = f.read()
        except FileNotFoundError:
            print(f"File not found at {self.path + fn}. Try again.")
        return prv_key

    def load_shared_key(self, fn: str = 'shared.key'):
        """Loads shared secret from file."""

        shr_key = None
        try:
            with open(self.path + fn, 'rb') as f:
                f.read()
        except FileNotFoundError:
            print(f"File not found at {self.path + fn}. Try again.")
        return shr_key

    #=== Public Boxes ===#
    def make_public_box(self, prv_key: PrivateKey,
                        ur_pub_key: PublicKey) -> Box:
        """Make public box from one private, one public. Usually different."""

        box = Box(prv_key, ur_pub_key)
        return box

    def encrypt(self, box: Box, bytes_msg: bytes) -> bytes:
        """Encrypt from a public box."""

        cipher_msg = box.encrypt(bytes_msg)
        return cipher_msg

    def decrypt(self, box: Box, cipher_msg: bytes) -> str:
        """Decrypt a bytes message with a public box."""

        plaintext = box.decrypt(cipher_msg)
        return plaintext.decode()

    #=== Secret Box ===#
    def make_secret_box(self, key: hex) -> SecretBox:
        """Create box with shared key opening."""
        sec_box = SecretBox(key)
        return sec_box

    def put_in_secret_box(self, secret_box: SecretBox, bytes_msg: bytes) -> hex:
        """Creates encrypted message with secret box."""
        cipher_txt = secret_box.encrypt(bytes_msg)
        assert len(cipher_txt) == len(
            bytes_msg) + secret_box.NONCE_SIZE + secret_box.MACBYTES
        return cipher_txt

    def open_secret_box(self, secret_box: SecretBox, ciphertext: hex) -> str:
        """Decryptes secret box contents."""
        cleartext = secret_box.decrypt(ciphertext)
        return cleartext.decode()

    #=== Generate Shared Keys ===#
    def gen_shared_key(self, box: Box, fn: str = 'shared.key') -> bytes:
        """Generates a shared secret from a public box. Returns Hexbytes."""

        path = self.path
        self.check_dir(path)
        shr_key = box.shared_key()
        # Writes as base64 bytes.
        with open(path + fn, 'wb') as f:
            f.write(Base64Encoder().encode(shr_key))

        return shr_key

    #=== Signing ===#
    def generate_signing_keys(self,
                              fn: str = 'signing.key'
                             ) -> (SigningKey, VerifyKey):
        """Generates key for signing and authenticating.
        
        A valid digital signature gives a recipient reason to believe that the
        message was created by a known sender such that they cannot deny
        sending it (authentication and non-repudiation) and that the message
        was not altered in transit (integrity).

        This must be protected and remain secret. Anyone who knows the value of
        your SigningKey or its seed can masquerade as you.
        """
        signing_key = SigningKey.generate()
        with open(self.path + fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(signing_key.encode(encoder=Base64Encoder))

        verify_key = signing_key.verify_key
        with open(self.path + fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(verify_key.encode(encoder=Base64Encoder))

        return signing_key, verify_key

    def sign(self, signing_key: SigningKey, bytes_msg: bytes) -> SignedMessage:
        """Signs payload."""
        signed_payload = signing_key.sign(bytes_msg)
        return signed_payload

    def verify(self, verify_key: VerifyKey,
               signed_payload: SignedMessage) -> bytes:
        """Returns error if signed payload is forged. Message if verified."""
        verified_bytes = verify_key.verify(signed_payload)
        return verified_bytes

    def make_bytes_verify_key_from_sender(self,
                                          verify_key_bytes: bytes) -> VerifyKey:
        """Convert if sender has sent verification key as bytes."""
        verify_key = VerifyKey(verify_key_bytes)
        return verify_key

    def make_hex_verify_key_from_sender(self, verify_key_hex: hex) -> VerifyKey:
        """Convert if sender has sent verification key as hex."""
        verify_key = VerifyKey(verify_key_hex, encoder=HexEncoder)
        return verify_key

    def make_b64_verify_key_from_sender(self,
                                        verify_key_b64: bytes) -> VerifyKey:
        """Convert if sender has sent verification key as b64.
        
        Be sure to decode the signed package as well with Base64Encoder.decode()
        """
        verify_key = VerifyKey(verify_key_b64, encoder=Base64Encoder)
        return verify_key

    #=== General Utilities ===#
    def check_dir(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)


if __name__ == "__main__":
    salt = SaltCipher()
    box = salt.make_public_box(salt.prv_key, salt.pub_key)
    msg = "hello how are you?"
    cipher_txt = salt.encrypt(box, msg.encode())
    print(cipher_txt)
    decoded = salt.decrypt(box, cipher_txt)
    print(decoded)
    shared_key = salt.gen_shared_key(box)
    print(shared_key)

    enc_shared_key = Base64Encoder.encode(shared_key)
    print('encoded shared key:', enc_shared_key)

    enc_prv_key = Base64Encoder.encode(salt.load_prv_key())
    print('encoded private key:', enc_prv_key)

    enc_pub_key = Base64Encoder.encode(salt.load_pub_key())
    print('encoded private key:', enc_pub_key)

    secret_box = salt.make_secret_box(shared_key)
    encrypted = salt.put_in_secret_box(secret_box, msg.encode())
    print(encrypted)
    decrypted = salt.open_secret_box(secret_box, encrypted)
    print(decrypted)
    signing_key, verify_key = salt.generate_signing_keys()
    signed = salt.sign(signing_key, decrypted.encode())
    print(signed)

    # message_bytes = salt.verify(verify_key.encode(), signed)
    message_bytes = salt.verify(verify_key, signed)
    print(message_bytes)

    forged = signed[:-1] + bytes([int(signed[-1]) ^ 1])
    # verify_key.verify(forged)
    # salt.verify(verify_key.encode(), signed)
