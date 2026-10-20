import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """Run in an empty folder. Keys get written to relative paths."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


class FakeSock:
    """Stands in for serv_sock. Feeds canned bytes, keeps what gets sent."""

    def __init__(self, incoming: bytes = b''):
        self.incoming = incoming
        self.sent = b''

    def recv(self, n):
        chunk, self.incoming = self.incoming[:n], self.incoming[n:]
        return chunk

    def send(self, data):
        self.sent += data
        return len(data)


def frame(msg) -> bytes:
    """Length prefix + message, the part after the type byte."""
    if isinstance(msg, bytes):
        msg = msg.decode()
    return f'{len(msg):04}{msg}'.encode()


def packets(raw: bytes):
    """Splits sent bytes back into (type, message) pairs."""
    out = []
    while raw:
        typ = raw[:1].decode()
        size = int(raw[1:5])
        out.append((typ, raw[5:5 + size]))
        raw = raw[5 + size:]
    return out
