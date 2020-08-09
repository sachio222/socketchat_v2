#### secure-cli-socketchat-python-v1
# Secure CLI Socket Chat (BETA)
### Street name: Encryptochat / Cryptochat
======

You don't need messenger. **Secure CLI Socket Chat** connects you directly to a host server that you can set up with a single command (```python3 server.py```). Allows you to chat with other terminals on your network, or around the world. The unencrypted server.py requires no additional libraries and is the software size equivalent of a postage stamp. It's so lightweight it will run almost anywhere, even a Raspberry Pi1! The encrypted version is also very small, but requires the quick pip install of a Python crytograpic package, and is currently using shared key encryption ([Fernet](https://medium.com/coinmonks/if-youre-struggling-picking-a-crypto-suite-fernet-may-be-the-answer-95196c0fec4b)). More levels of encryption to come. 

## Features:
* Secure, client-side encryption/decryption using Fernet cipher (PGP, blowfish coming soon).
* Use it on your own LAN to chat between computers, or across the world with friends.
* Direct message or multiple chat-client connections.
* Simple usage. Just spin up server.py, and use client.py to begin chatting. 
* Secure chat: Encrypt your traffic using symmetric encryption.
* Customize max client count.
* Works out of box with Python 3.x, no libraries required (Secure chat requires addl libraries).
* Tiny filesize footprint and runs with barely any setup.
* Monitor unencrypted chats on your server.
* Audio alerts controllable with mute() or unmute().
* Exit chat with exit().

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=diamondhawk&url=https://github.com/sachio222/socketchat_v1)

## Usage

#### No-encrypt chat (only 2 files needed: server.py, client.py)
1. Spin up server.py on any machine, define port number to listen on. 
2. Open client.py, connect to defined port.
3. Chat.

*Note: in the unencrypted chat, you only need 2 files. ```server.py``` and ```client.py```. Everything else is for the encrypted chat. 

#### Encrypted chat
1. Spin up server.py same as above. 
2. Run keygen-fernet.py to generate secret.key
3. Share this SAME secret.key with any person you want to be able to read your messages, and have them place it in their socketchat folder.
4. Open sec-client.py, connect to defined port. 
5. Chat.

## Usage

```mute()```

```unmute()```

```status()``` Shows who's in the room at the moment. 

```ping``` Sends a ping request to the server.

```exit()``` Quits the client. 

## Contributors
J. Krajewski


### Third party libraries
https://pypi.org/project/cryptography/

Install using ``` pip install cryptography```

## License 
* see [LICENSE](https://github.com/username/sw-name/blob/master/LICENSE.md) file

## Version 
* Version 1.0

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

