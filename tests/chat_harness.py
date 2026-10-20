"""Drives a real server.py and client.py over stdin/stdout.

Used by test_end_to_end.py. Every process started here gets killed on exit.
"""

import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSI = re.compile(r'\x1b\[[0-9;]*[A-Za-z]|\x07|\r')


def free_port() -> int:
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def copy_repo(dst, src=REPO) -> str:
    """Copy of the app without keys, git data or tests."""
    shutil.copytree(src,
                    dst,
                    ignore=shutil.ignore_patterns('.git', '__pycache__',
                                                  'keys', 'tests', '*.pyc'))
    return str(dst)


class Proc:
    """One running script. Collects everything it prints."""

    def __init__(self, name, args, cwd, python=sys.executable):
        self.name = name
        self.p = subprocess.Popen([python, '-u', *args],
                                  cwd=cwd,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        self._raw = b''
        self._lock = threading.Lock()
        self._reader = threading.Thread(target=self._read, daemon=True)
        self._reader.start()

    def _read(self):
        fd = self.p.stdout.fileno()
        while True:
            try:
                chunk = os.read(fd, 4096)
            except OSError:
                break
            if not chunk:
                break
            with self._lock:
                self._raw += chunk

    @property
    def text(self) -> str:
        with self._lock:
            raw = self._raw
        return ANSI.sub('', raw.decode(errors='replace'))

    def mark(self) -> int:
        return len(self.text)

    def send(self, line: str):
        self.p.stdin.write(line.encode() + b'\n')
        self.p.stdin.flush()

    def wait_for(self, pattern, timeout=20, since=0) -> re.Match:
        deadline = time.time() + timeout
        while time.time() < deadline:
            m = re.search(pattern, self.text[since:])
            if m:
                return m
            if self.p.poll() is not None:
                time.sleep(0.2)  # Let the reader catch the last bytes.
                m = re.search(pattern, self.text[since:])
                if m:
                    return m
                break
            time.sleep(0.05)
        raise AssertionError(
            f'{self.name} never printed {pattern!r}. Output:\n{self.text}')

    def kill(self):
        if self.p.poll() is None:
            self.p.kill()
        self.p.wait(timeout=10)
        for f in (self.p.stdin, self.p.stdout):
            try:
                f.close()
            except Exception:
                pass


class Chat:
    """One server plus any number of clients. Kills them all on exit."""

    def __init__(self, port, python=sys.executable):
        self.port = port
        self.python = python
        self.procs = []

    def server(self, cwd) -> Proc:
        s = Proc('server', ['server.py', 'debug', str(self.port)], cwd,
                 self.python)
        self.procs.append(s)
        s.wait_for('Waiting for secure connections')
        return s

    def client(self, handle, cwd) -> Proc:
        c = Proc(handle, ['client.py', '-P', str(self.port)], cwd, self.python)
        self.procs.append(c)
        c.wait_for('Enter hostname of server')
        c.send('')  # Take the default host.
        c.wait_for('Choose a handle')
        c.send(handle)
        c.wait_for("You're in")
        return c

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        for p in self.procs:
            p.kill()
