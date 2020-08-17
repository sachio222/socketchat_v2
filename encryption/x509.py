"""
https://cryptography.io/en/latest/x509/tutorial/
Certificate Signing Requests (CSR) 6 steps. 
1. Generate private/public key pair.
2. Request certificate, signed by key.
3. Give CSR to Certificate Authority (CA)
4. CA validates that you own what you asked for a cert for.
5. CA gives cert signed by them, which identifies public key, and the
    authenticated resource.
6. Configure server to use that cert, combined with private key to 
    server traffic.
"""

import os
import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


class X509():

    def __init__(self):
        self.rsa_key_path = 'encryption/keys/TLS/rsa_key.pem'
        self.cert_path = 'encryption/keys/TLS/certificate.pem'

        key = self.generate_private_rsa_key(self.rsa_key_path)

        self.self_sign_cert(key)

    def generate_private_rsa_key(self, path):
        # Generate a private RSA key.
        key = rsa.generate_private_key(public_exponent=65537,
                                       key_size=2048,
                                       backend=default_backend())

        # Write key
        folders = os.path.dirname(path)
        if not os.path.exists(folders):
            os.makedirs(folders)

        with open(path, 'wb') as f:
            f.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.BestAvailableEncryption(
                        b'pw')))
        return key

    def load_private_rsa_key(self, path):
        #probably won't work.
        # serialization.load_pem_private_key()
        pass

    def self_sign_cert(self, key):
        # Self signing.
        # Provide signing details.
        subject = issuer = x509.Name([
            # Provide various details about who we are for request from CA.
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'California'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'San Mateo'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Company Inc.'),
            x509.NameAttribute(NameOID.COMMON_NAME, u'ubuntu')
        ])

        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(
            issuer).public_key(
                # Send request with public key.
                key.public_key()).serial_number(
                    x509.random_serial_number()).not_valid_before(
                        datetime.datetime.utcnow()).not_valid_after(
                            datetime.datetime.utcnow() +
                            datetime.timedelta(days=10)).add_extension(
                                x509.SubjectAlternativeName(
                                    [x509.DNSName(u'ubuntu')]),
                                critical=False
                                # Sign certificate with private key
                            ).sign(key, hashes.SHA256(), default_backend())
        # Write certificate to disk
        with open(self.cert_path, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))


if __name__ == "__main__":
    x509 = X509()
    # key = x509.generate_private_rsa_key()
    # x509.self_sign_cert(key)
