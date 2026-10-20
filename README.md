# socketchat v2

A chat you run from the terminal. One person starts a small server, friends connect to it from their own machines, and anyone who wants privacy can switch to encrypted messages with `/trust`.

I built it in 2020 to learn how sockets and encryption work together. It works, and the code is small enough to read in an afternoon. It is a learning project, so don't use it for anything you need to keep secret: "Before you rely on it" below lists exactly where it falls short. [socketchat v3](https://github.com/sachio222/socketchat_v3) is the next step, with authenticated ciphers and a cleaner design.

## What it does

- Plain group chat between everyone connected to one server.
- Encrypted chat between two people after `/trust`. The server passes along scrambled text it can't read.
- TLS between each client and the server. TLS is the same transport encryption web browsers use.
- Add-ons for weather, moon phase, maps, Wikipedia, Urban Dictionary, number trivia and NASA's daily Earth images.

## Install

You need Python 3.10 or newer. It was last tested on Python 3.14 on an Apple Silicon Mac.

```
git clone https://github.com/sachio222/socketchat_v2
cd socketchat_v2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run it

### 1. Start the server

```
python server.py debug
```

That runs the server on your own machine (127.0.0.1) at port 12222. Add a number to use another port: `python server.py debug 12345`. Leave off `debug` and the server asks for a port, then listens on your computer's network address, so friends on your Wi-Fi can join.

Each time it starts, the server makes a fresh TLS key and certificate in `encryption/keys/TLS/`. Only your user account can read the key.

### 2. Give each client the server's certificate

Copy `encryption/keys/TLS/certificate.pem` from the server's folder into the same place in each client's folder. A client you run from the server's own folder already has it. If it's missing, the client tells you where to get it.

### 3. Connect

```
python client.py -H 127.0.0.1 -P 12222
```

Leave off `-H` or `-P` and the client asks, with 127.0.0.1 and 12222 filled in. Pick a handle and start typing.

## Encrypted chat

Chat starts plain. To encrypt with someone, say bob:

1. Type `/trust bob`.
2. bob sees "Wanna trust @alice (Y/N)?" and types `y`.
3. You both see "Trust acquired." Messages between you are now encrypted. They show in green, with an @ before the handle.

How it works: when you join, your client makes a key pair with NaCl, a well-known encryption library, and gives the server your public key. On `/trust`, the server swaps public keys between you and bob, and each side works out the same shared secret. Your client then makes a fresh AES-256 key for the conversation, seals it with that shared secret, and sends it to bob. The server only ever sees scrambled data.

You can run two clients from one folder. Each keeps its keys in `encryption/keys/clients/<handle>/`.

## Before you rely on it

- **The server hands out public keys, and nothing checks them.** A dishonest server could swap in its own key and read everything. socketchat v3 has the same gap.
- **Clients don't verify the server's certificate.** The client loads it but accepts any server.
- **No tamper check.** AES-256 runs in CBC mode without a message authentication code, so a message changed on the way wouldn't get caught. socketchat v3 fixes this with ChaCha20-Poly1305.
- **One conversation key at a time.** Trusting a second person replaces the key you share with the first.
- **The server sees who talks to whom.** Handles travel in the clear.
- **Accented letters can break plain messages.** The message length counts characters, not bytes. socketchat v3 fixes this.
- **Files go unencrypted.** `/sendfile` hasn't been retested since 2020.
- **Goober mode.** `-g` keeps your own messages plain even after `/trust`.

## Commands

| Command | What it does |
|---|---|
| `/help` | Lists every command and add-on. |
| `/trust <handle>` | Starts encrypted chat with that person. |
| `/status` | Shows who's online. |
| `/mute`, `/unmute` | Turns chat sounds off and on. |
| `/sendfile` | Sends a file to one person, unencrypted. |
| `/exit` | Quits the client. |

Add-ons: `/weather <place>`, `/moon`, `/map <place>`, `/wikipedia <term>` (or `/wp`), `/urband <term>`, `/mathtrivia <number>` and `/epic`. `/mathtrivia` needs a free key from rapidapi.com, set as `RAPIDAPI_KEY`.

`keygen_fernet.py` writes a shared Fernet key to `encryption/keys/fernet/secret.key`. It's left over from v1's shared-key mode. `/trust` doesn't need it.

## Tests

```
pip install pytest
python -m pytest
```

One test starts a real server and two clients on a free port, checks plain and encrypted messages both ways, and shuts them down.

## Troubleshooting

On a Mac, `socket.gaierror: [Errno 8] nodename nor servname provided, or not known` usually clears if you turn Sharing on and off again in System Settings ([details](https://stackoverflow.com/a/53382881/5369711)).

## Credits

Jake Krajewski and M. Holcombe.

Built on [PyNaCl](https://pynacl.readthedocs.io/) and [cryptography](https://pypi.org/project/cryptography/).

## License

MIT. See [LICENSE.md](LICENSE.md).
