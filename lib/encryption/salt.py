import os
import nacl.utils
from nacl.secret import SecretBox
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder, HexEncoder, RawEncoder
from nacl.signing import SigningKey, SignedMessage, VerifyKey

import config.filepaths as paths

PATH = paths.nacl_keys


class NaclCipher():
    """Based on the python fork of nacl's libsodium framework.
    https://pynacl.readthedocs.io/
    
    The salt cipher involves state of the art encryption for assymetric
    encryption between users with the exchange of public keys and the
    creation of a shared secret. Also allows for signing/verification.
    """

    def __init__(self, path: str = PATH):
        self.path = path
        self.check_dir(self.path)
        self.prv_key, self.pub_key = self.generate_keys()

    @staticmethod
    def generate_keys(path: str = PATH,
                      prv_fn: str = 'private.key',
                      pub_fn: str = 'public.key') -> tuple:
        """Generate and save key pair. Use Base64Encoder to write to bytes."""

        # Generate a private key.
        prv_key = PrivateKey.generate()
        with open(path + prv_fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(prv_key.encode(encoder=Base64Encoder))

        # Get public key from private.
        pub_key = prv_key.public_key
        with open(path + pub_fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(pub_key.encode(encoder=Base64Encoder))

        return prv_key, pub_key

    def make_shared_key_from_new_box(self,
                                     pubk: PublicKey,
                                     prvk: PrivateKey = None,
                                     box: Box = None) -> tuple:
        prvk = prvk or self.load_prv_key()
        prvk = self.decode_b64(prvk, 'private')

        if not box:
            box = self.make_public_box(prvk, pubk)
            shrk = self.gen_shared_key(box)
            with open(self.path + 'shared.key', 'wb') as f:
                f.write(shrk)

            return shrk, box

    def encode_b64(self, key: bytes, key_type: str = None) -> bytes:
        """Change key to base64"""
        if key_type != 'shared':
            b64_key = key.encode(encoder=Base64Encoder)
        else:
            b64_key = Base64Encoder.encode(key)
        return b64_key

    def decode_b64(self, b64_key: bytes, key_type: str = "public"):
        """Decode from base64 to key objects.
        
        Example
            decoded_prv_key = PrivateKey(b64_key, encoder=Base64Encoder)
        """
        if key_type != 'shared':
            keys = {'public': PublicKey, 'private': PrivateKey}
            key = keys.get(key_type,
                           print("valid options: public, private, shared."))(
                               b64_key, encoder=Base64Encoder)
        else:
            key = Base64Encoder.decode(b64_key)
        return key

    @staticmethod
    def load_pub_key(path: str = PATH, fn: str = 'public.key') -> PublicKey:
        """Returns PublicKey as Base64. Use encoder=Base64Encoder for bytes."""

        pub_key = None
        try:
            with open(path + fn, 'rb') as f:
                pub_key = f.read()
        except FileNotFoundError:
            print(f"File not found at {path + fn}. Try again.")
        return pub_key

    @staticmethod
    def load_prv_key(path: str = PATH, fn: str = 'private.key') -> PrivateKey:
        """Returns PrivateKey as Base64. Use encoder=Base64Encoder for bytes."""

        prv_key = None
        try:
            with open(path + fn, 'rb') as f:
                prv_key = f.read()
        except FileNotFoundError:
            print(f"File not found at {path + fn}. Try again.")
        return prv_key

    @staticmethod
    def load_shared_key(path: str = PATH, fn: str = 'shared.key'):
        """Loads shared secret from file."""

        shr_key = None
        try:
            with open(path + fn, 'rb') as f:
                f.read()
        except FileNotFoundError:
            print(f"File not found at {path + fn}. Try again.")
        return shr_key

    #=== Public Boxes ===#
    @staticmethod
    def make_public_box(prv_key: PrivateKey, ur_pub_key: PublicKey) -> Box:
        """Make public box from one private, one public. Usually different."""
        try:
            prv_key = PrivateKey(prv_key, encoder=Base64Encoder)
            ur_pub_key = PublicKey(ur_pub_key, encoder=Base64Encoder)
        except:
            pass
        box = Box(prv_key, ur_pub_key)
        return box

    def encrypt(self, box: Box, bytes_msg: bytes) -> bytes:
        """Encrypt from a public box."""
        try:
            cipher_msg = box.encrypt(bytes_msg)
            return cipher_msg
        except:
            return ('Failed to encrypt. U r not covered. Quit and try again.')

    def decrypt(self, box: Box, cipher_msg: bytes) -> str:
        """Decrypt a bytes message with a public box."""
        plaintext = box.decrypt(cipher_msg)
        return plaintext.decode()

    #=== Secret Box ===#
    def make_secret_box(self, shr_key: hex) -> SecretBox:
        """Create box with shared key opening."""
        sec_box = SecretBox(shr_key)
        return sec_box

    def put_in_secret_box(self, secret_box: SecretBox, bytes_msg: bytes) -> hex:
        """Creates encrypted message with secret box."""
        cipher_txt = secret_box.encrypt(bytes_msg)
        assert len(cipher_txt) == len(
            bytes_msg) + secret_box.NONCE_SIZE + secret_box.MACBYTES
        return cipher_txt

    def open_secret_box(self, secret_box: SecretBox, cipher_text: hex) -> str:
        """Decryptes secret box contents."""
        cleartext = secret_box.decrypt(cipher_text)
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
    @staticmethod
    def generate_signing_keys(path: str = PATH,
                              sgn_fn: str = 'signing.key',
                              ver_fn: str = 'verify.key') -> tuple:
        """Generates key for signing and authenticating.
        
        A valid digital signature gives a recipient reason to believe that the
        message was created by a known sender such that they cannot deny
        sending it (authentication and non-repudiation) and that the message
        was not altered in transit (integrity).

        This must be protected and remain secret. Anyone who knows the value of
        your SigningKey or its seed can masquerade as you.
        """
        signing_key = SigningKey.generate()
        with open(path + sgn_fn, 'wb') as f:
            # Writes as base64 bytes.
            f.write(signing_key.encode(encoder=Base64Encoder))

        verify_key = signing_key.verify_key
        with open(path + ver_fn, 'wb') as f:
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
    # Usage Examples
    # Init and gen keys.
    salt = NaclCipher()

    # Access created key vars as key objects.
    print(salt.prv_key)
    print(salt.pub_key)
    # Access keys from file, stored as b64.
    prv_key = salt.load_prv_key()
    pub_key = salt.load_pub_key()
    print(prv_key)
    print(pub_key)
    # Convert back to key objects.
    prv_key = PrivateKey(prv_key, encoder=Base64Encoder)
    pub_key = PublicKey(pub_key, encoder=Base64Encoder)
    # Or use helper function
    # pub_key = salt.decode_b64(pub_key, 'public')
    # Make a pub box with key objects.
    box = salt.make_public_box(prv_key, pub_key)
    msg = "hello how are you?"
    # Generate shared key from box object.
    shared_key_orig = salt.gen_shared_key(box)
    print('shared key:', shared_key_orig)
    # Convert shared key to b64.
    shared_key = Base64Encoder.encode(shared_key_orig)
    print('shared key to b64:', shared_key)
    # Convert key back to key object using helper func.
    shared_key2 = salt.decode_b64(shared_key, 'shared')
    print('shared key back:', shared_key2)
    print(shared_key_orig == shared_key2)
    print('========END==========')

    # Get encoded message from box.
    cipher_txt = salt.encrypt(box, msg.encode())
    print('cipher_text is\n', cipher_txt)
    cipher_txt64 = Base64Encoder.encode(cipher_txt)
    print(cipher_txt64)
    cipher_txtstr = cipher_txt64.decode()
    print(cipher_txtstr)
    cipher_txt_cat = '00555' + cipher_txtstr
    print(cipher_txt_cat)
    ciphertxt_split = cipher_txt_cat.replace('00555', '')
    print(ciphertxt_split)
    cipher_txt64 = Base64Encoder.decode(ciphertxt_split)
    print(cipher_txt64)
    # Decrypt message from box that created it.
    decrypted = salt.decrypt(box, cipher_txt)
    print(decrypted)
    # exit()

    # # Encode shared key to b64.
    # enc_shared_key = Base64Encoder.encode(shared_key)
    # print('encoded shared key:', enc_shared_key)

    # print('original key:', salt.prv_key)
    # print('encoded private key:',)
    # print('=========here=======')
    # # Make a secret box from a shared key.
    # secret_box = salt.make_secret_box(shared_key)
    # # Encrypt something with the secret box.
    # encrypted = salt.put_in_secret_box(secret_box, msg.encode())
    # print(encrypted)
    # # Decrypt that thing with the same box.
    # decrypted = salt.open_secret_box(secret_box, encrypted)
    # print(decrypted)
    # # Create sign/verify keys.
    # signing_key, verify_key = salt.generate_signing_keys()
    # # Created signed document.
    # signed = salt.sign(signing_key, decrypted.encode())
    # print(signed)
    # # message_bytes = salt.verify(verify_key.encode(), signed)
    # # Verify signed document.
    # message_bytes = salt.verify(verify_key, signed)
    # print(message_bytes)
    # # Show that its forged.
    # forged = signed[:-1] + bytes([int(signed[-1]) ^ 1])
    # # verify_key.verify(forged)
    # # salt.verify(verify_key.encode(), signed)

    # import nacl.utils
    # from nacl.public import PrivateKey, Box

    # Generate Bob's private key, which must be kept secret
    skbob = PrivateKey.generate()
    print('pvk', skbob)

    # Bob's public key can be given to anyone wishing to send
    #   Bob an encrypted message
    pkbob = skbob.public_key

    # Alice does the same and then Alice and Bob exchange public keys
    skalice = PrivateKey.generate()
    pkalice = skalice.public_key

    print('pvk', skalice)

    # Bob wishes to send Alice an encrypted message so Bob must make a Box with
    #   his private key and Alice's public key
    bob_box = Box(skbob, pkalice)
    # bobshrk = salt.gen_shared_key(bob_box)
    bobshrk = salt.gen_shared_key(bob_box)
    print('bob share', bobshrk)

    # This is our message to send, it must be a bytestring as Box will treat it
    #   as just a binary blob of data.
    message = b"Love all humans"

    encrypted = bob_box.encrypt(message)

    # Alice creates a second box with her private key to decrypt the message
    alice_box = Box(skalice, pkbob)
    aliceshrk = salt.gen_shared_key(alice_box)
    print('alice share', aliceshrk)

    # Decrypt our message, an exception will be raised if the encryption was
    #   tampered with or there was otherwise an error.
    plaintext = alice_box.decrypt(encrypted)
    print(plaintext.decode('utf-8'))
