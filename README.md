#### secure-cli-socketchat-python-v1
# Secure CLI Socket Chat (BETA)
### Street name: Encryptochat / Cryptochat
======

You don't need messenger. **Secure CLI Socket Chat** 

## Features:
* Secure, client-side encryption/decryption using NaCl (pynacl).
* Use it on your own LAN to chat between computers, or across the world with friends.
* Direct message or multiple chat-client connections.
* Secure chat: Encrypt your traffic using recommended assymetric key encryption.
* Tiny filesize footprint and runs with barely any setup.
* Monitor unencrypted chats on your server.
* Addons and features added continually.

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=diamondhawk&url=https://github.com/sachio222/socketchat_v1)

## Install

Needs Python 3.10 or newer. Tested on Python 3.14 on an Apple Silicon Mac.

```
git clone https://github.com/sachio222/socketchat_v2
cd socketchat_v2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

#### 1. Start the server

```
python server.py debug
```

That runs the server on 127.0.0.1, port 12222. Add a number for another port: `python server.py debug 12345`. Leave off `debug` and it asks for a port and listens on your computer's network address, so friends on your LAN can join.

Every time it starts, the server makes a new TLS key and certificate in `encryption/keys/TLS/`. The key has no pass phrase. Only your user account can read it.

#### 2. Give each client the server's certificate

Copy `encryption/keys/TLS/certificate.pem` from the server's folder into the same spot in each client's folder. A client run from the server's own folder already has it. Without it, the client stops and tells you where to get it.

#### 3. Connect

```
python client.py -H 127.0.0.1 -P 12222
```

Leave off `-H` or `-P` and the client asks, with 127.0.0.1 and 12222 as the defaults. Then pick a handle and start typing.

#### Encrypted chat

Chat starts plain. To encrypt with someone, say bob:

1. Type `/trust bob`.
2. bob sees "Wanna trust @alice (Y/N)?" and types `y`.
3. You both see "Trust acquired." From then on, messages between you are encrypted, and they show up in green with an @ in front of the handle.

Under the hood, each client makes a NaCl key pair (public key encryption from the PyNaCl library) when it joins and gives the server its public key. On `/trust`, the server swaps public keys between you and bob, and each of you works out the same shared secret from them. Your client makes a fresh AES256 session key, locks it in a NaCl secret box with that secret, and sends it to bob. The server passes along ciphertext and never holds the session key.

Run two clients from one folder if you like. Each keeps its keys in `encryption/keys/clients/<handle>/`.

Good to know before you trust it with anything big:

* Handles still go through the server in plaintext, so the server knows who's talking.
* After `/trust`, everything you send is encrypted, so anyone else in the room sees hex.
* The server hands out the public keys, and there's no fingerprint check yet, so you're trusting the server not to swap them.
* The client loads the certificate but doesn't verify the server against it yet.
* AES256 runs in CBC mode without a MAC (message authentication code), so a message changed in transit wouldn't get caught.
* `-g` (goober mode) keeps your own messages plain, even after `/trust`.

`keygen_fernet.py` writes a new Fernet key (a shared secret key from the cryptography library) to `encryption/keys/fernet/secret.key`. That's from v1's shared-key mode, and `/trust` doesn't need it.

## Commands

```/help``` Shows every command, add-ons too.

```/trust <handle>``` Starts encrypted chat with that person.

```/mute```

```/unmute```

```/status``` Shows who's in the room at the moment. 

```/exit``` Quits the client. 

```/sendfile``` Sends file (currently unencrypted) to selected user.

## Tests

```
pip install pytest
python -m pytest
```

The end to end test starts a real server and two clients on a free port, and kills them when it's done.

## Contributors
J. Krajewski
M. Holcombe


### Third party libraries
https://pypi.org/project/cryptography/

https://pynacl.readthedocs.io/

Both come with `pip install -r requirements.txt`.

## License 
* see [LICENSE](https://github.com/username/sw-name/blob/master/LICENSE.md) file

## Version 
* Version 1.1

## Troubleshooting
Currently tested on MacOSX and Linux. 

Error:
```socket.gaierror: [Errno 8] nodename nor servname provided, or not known```

System: Mac

Solution: [Enable Sharing Permissions, then Disable](https://stackoverflow.com/a/53382881/5369711)

## Contact
#### Developer/Company

* Twitter: [@jakekrajewski](https://twitter.com/jakekrajewski "@jakekrajewski")
* Medium: [@Jakekrajewski](https://medium.com/@Jakekrajewski)

