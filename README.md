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

## Usage

#### Encrypted chat
0. Available soon...
1. Spin up server.py same as above. 
2. Run keygen-fernet.py to generate secret.key
3. Share this SAME secret.key with any person you want to be able to read your messages, and have them place it in their socketchat folder.
4. Open sec-client.py, connect to defined port. 
5. Chat.

## Usage

```/mute```

```/unmute```

```/status``` Shows who's in the room at the moment. 

```ping``` Sends a ping request to the server.

```/exit``` Quits the client. 

```/sendfile``` Sends file (currently unencrypted) to selected user.

## Contributors
J. Krajewski
M. Holcombe


### Third party libraries
https://pypi.org/project/cryptography/

Install using ``` pip install cryptography```

https://pynacl.readthedocs.io/en/1.4.0/

Install using ```pip install pynacl```

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

