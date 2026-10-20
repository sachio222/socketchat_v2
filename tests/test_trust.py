"""/trust between two clients, run by hand through the client handlers.

The server's part is faked: it hands each side the other's public key,
then forwards alice's 'x' (the boxed AES256 session key) to bob.
"""

from pathlib import Path

import pytest
from nacl.encoding import Base64Encoder
from nacl.public import PrivateKey

from conftest import FakeSock, frame, packets

import client


def make_client(monkeypatch, handle, allow_encryption=True):
    """A client that picked `handle` and just got the server's welcome."""
    c = client.Client(muted=True)
    c.allow_encryption = allow_encryption
    c.handle = handle  # What sender() remembers when you type your handle.
    sock = FakeSock(frame("You're in. Welcome to the underground."))
    monkeypatch.setattr(client, 'serv_sock', sock, raising=False)
    c._w_handler(sock)
    sent = dict(packets(sock.sent))
    c.test_pub_key = sent['P']  # Public key it uploaded to the server.
    return c


def trust(monkeypatch, alice, bob):
    """alice ran /trust bob and bob said y."""
    # Server sends bob alice's key as 'k'.
    b_sock = FakeSock(frame(alice.test_pub_key))
    monkeypatch.setattr(client, 'serv_sock', b_sock, raising=False)
    bob._lil_k_handler(b_sock)

    # Server sends alice bob's key as 'K'. alice answers with the session key.
    a_sock = FakeSock(frame(bob.test_pub_key))
    monkeypatch.setattr(client, 'serv_sock', a_sock, raising=False)
    alice._k_handler(a_sock)
    typ, boxed_key = packets(a_sock.sent)[0]
    assert typ == 'x'

    # Server forwards it to bob.
    x_sock = FakeSock(frame(boxed_key))
    monkeypatch.setattr(client, 'serv_sock', x_sock, raising=False)
    bob._lil_x_handler(x_sock)


def received(capsys, c, sender, payload):
    """What c prints when the server relays `payload` from `sender`."""
    if isinstance(payload, str):
        payload = payload.encode()
    sock = FakeSock(frame(f'{sender}: '.encode() + payload))
    monkeypatch_serv_sock(sock)
    capsys.readouterr()
    c._m_handler(sock)
    return capsys.readouterr().out


def monkeypatch_serv_sock(sock):
    # _m_handler reads from the module's serv_sock, like the real client.
    client.serv_sock = sock


def test_alice_to_bob_decrypts_after_trust(workdir, monkeypatch, capsys):
    alice = make_client(monkeypatch, 'alice')
    bob = make_client(monkeypatch, 'bob')
    trust(monkeypatch, alice, bob)

    payload = alice.encrypt_outgoing('meet at noon')
    assert b'meet at noon' not in payload

    out = received(capsys, bob, 'alice', payload)
    assert '@alice:' in out
    assert 'meet at noon' in out


def test_bob_to_alice_decrypts_after_trust(workdir, monkeypatch, capsys):
    alice = make_client(monkeypatch, 'alice')
    bob = make_client(monkeypatch, 'bob')
    trust(monkeypatch, alice, bob)

    payload = bob.encrypt_outgoing('bring snacks')
    assert b'bring snacks' not in payload

    out = received(capsys, alice, 'bob', payload)
    assert '@bob:' in out
    assert 'bring snacks' in out


def test_new_session_key_is_loaded_not_just_written(workdir, monkeypatch):
    alice = make_client(monkeypatch, 'alice')
    bob = make_client(monkeypatch, 'bob')
    old_alice_key, old_bob_key = alice.aes.key, bob.aes.key
    trust(monkeypatch, alice, bob)

    assert alice.aes.key == bob.aes.key
    assert alice.aes.key not in (old_alice_key, old_bob_key)
    assert len(alice.aes.key) == 32


def test_encryption_off_until_trust(workdir, monkeypatch):
    alice = make_client(monkeypatch, 'alice')
    assert alice.encrypt_flag is False
    assert alice.encrypt_outgoing('hello') == 'hello'


def test_goober_mode_stays_plain_after_trust(workdir, monkeypatch, capsys):
    alice = make_client(monkeypatch, 'alice')
    bob = make_client(monkeypatch, 'bob', allow_encryption=False)
    trust(monkeypatch, alice, bob)

    # bob asked for no encryption, so he sends plain...
    assert bob.encrypt_outgoing('plain from bob') == 'plain from bob'
    # ...but he can still read alice, who did encrypt.
    out = received(capsys, bob, 'alice', alice.encrypt_outgoing('hi bob'))
    assert 'hi bob' in out


def test_each_client_keeps_its_own_nacl_keys_in_one_folder(
        workdir, monkeypatch):
    alice = make_client(monkeypatch, 'alice')
    bob = make_client(monkeypatch, 'bob')

    assert alice.nacl.path != bob.nacl.path
    for c in (alice, bob):
        prv64 = (Path(c.nacl.path) / 'private.key').read_bytes()
        pub = PrivateKey(prv64, encoder=Base64Encoder).public_key
        # The key on disk still matches the one this client uploaded.
        assert pub.encode(encoder=Base64Encoder) == c.test_pub_key


def test_session_key_files_are_per_handle(workdir, monkeypatch):
    alice = make_client(monkeypatch, 'alice')
    bob = make_client(monkeypatch, 'bob')
    trust(monkeypatch, alice, bob)

    assert alice.aes.key_path != bob.aes.key_path
    assert Path(alice.aes.key_path).exists()
    assert Path(bob.aes.key_path).exists()


@pytest.mark.parametrize('handle', ['../../evil', '/etc', 'a/b', '..'])
def test_handle_cannot_escape_key_folder(workdir, monkeypatch, handle):
    c = make_client(monkeypatch, handle)
    keys = (workdir / 'encryption' / 'keys').resolve()
    assert keys in Path(c.nacl.path).resolve().parents
    assert keys in Path(c.aes.key_path).resolve().parents
