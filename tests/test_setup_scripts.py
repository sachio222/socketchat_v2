"""Startup basics: keygen_fernet, the server's TLS key, the client's cert."""

import os
import ssl
import stat
import subprocess
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization

from conftest import REPO


def run_script(args, cwd, timeout=60, stdin=subprocess.DEVNULL):
    return subprocess.run([sys.executable, *args],
                          cwd=cwd,
                          stdin=stdin,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          text=True,
                          timeout=timeout)


def test_keygen_fernet_imports():
    import keygen_fernet  # noqa: F401  (used to die on `import Cipher`)


def test_keygen_fernet_writes_a_working_key(workdir):
    result = run_script([os.path.join(REPO, 'keygen_fernet.py')], workdir)
    assert result.returncode == 0, result.stdout

    key = (workdir / 'encryption/keys/fernet/secret.key').read_bytes()
    f = Fernet(key)
    assert f.decrypt(f.encrypt(b'hi')) == b'hi'


def test_tls_key_has_no_passphrase_and_is_private(workdir):
    import encryption.x509 as x509
    x509.X509()

    key_path = workdir / 'encryption/keys/TLS/rsa_key.pem'
    cert_path = workdir / 'encryption/keys/TLS/certificate.pem'

    # Owner read/write only.
    assert stat.S_IMODE(os.stat(key_path).st_mode) == 0o600
    serialization.load_pem_private_key(key_path.read_bytes(), password=None)

    def no_prompt():
        raise AssertionError('server asked for a PEM pass phrase')

    ctxt = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctxt.load_cert_chain(cert_path, key_path, password=no_prompt)


def test_tls_key_rewrite_keeps_0600(workdir):
    import encryption.x509 as x509
    key_path = workdir / 'encryption/keys/TLS/rsa_key.pem'
    key_path.parent.mkdir(parents=True)
    key_path.write_text('old')
    os.chmod(key_path, 0o644)

    x509.X509()
    assert stat.S_IMODE(os.stat(key_path).st_mode) == 0o600


def test_client_without_cert_says_where_to_get_it(workdir):
    # Port 9 (discard) never gets dialed: the cert check comes first.
    result = run_script(
        [os.path.join(REPO, 'client.py'), '-H', '127.0.0.1', '-P', '9'],
        workdir)

    assert result.returncode != 0
    assert 'Traceback' not in result.stdout, result.stdout
    assert 'encryption/keys/TLS/certificate.pem' in result.stdout
    assert 'server' in result.stdout.lower()
