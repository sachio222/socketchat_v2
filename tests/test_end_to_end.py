"""Real server, two real clients, all three in one folder."""

import re

from chat_harness import Chat, copy_repo, free_port


def test_plain_then_encrypted_both_ways(tmp_path):
    app = copy_repo(tmp_path / 'app')

    with Chat(free_port()) as chat:
        server = chat.server(app)
        alice = chat.client('alice', app)
        bob = chat.client('bob', app)

        # Default host is 127.0.0.1.
        alice.wait_for('Connected to 127.0.0.1')

        # Plain, both ways.
        alice.send('plain hello from alice')
        bob.wait_for('alice: plain hello from alice')
        server.wait_for('alice: plain hello from alice')
        bob.send('plain hello from bob')
        alice.wait_for('bob: plain hello from bob')
        server.wait_for('bob: plain hello from bob')

        # Trust.
        alice.send('/trust bob')
        bob.wait_for(r'Wanna trust @alice')
        bob.send('y')
        alice.wait_for('Trust acquired')
        bob.wait_for('Trust acquired')
        bob.wait_for('AES256 session key received')

        # Encrypted, both ways.
        seen = server.mark()
        alice.send('secret from alice')
        bob.wait_for('@alice: secret from alice')
        bob.send('secret from bob')
        alice.wait_for('@bob: secret from bob')

        # Server relays both, and only ever sees ciphertext.
        server.wait_for(r'alice: \S+', since=seen)
        server.wait_for(r'bob: \S+', since=seen)
        relayed = server.text[seen:]
        assert 'secret from' not in relayed
        for line in re.findall(r'(?:alice|bob): (\S+)', relayed):
            assert re.fullmatch(r'[0-9a-f]+', line), line

        # Nobody crashed along the way.
        for p in (server, alice, bob):
            assert 'Traceback' not in p.text, p.text
            assert 'CryptoError' not in p.text, p.text
