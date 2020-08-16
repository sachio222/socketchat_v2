# socket clent.

import socket, ssl


host = '192.168.68.143'
client_ctxt = ssl.create_default_context()

# client_ctxt.load_cert_chain('../certificate.pem', '../key.pem')
client_ctxt.check_hostname = False
client_ctxt.verify_mode = ssl.CERT_NONE
client_ctxt.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
client_ctxt.options |= ssl.OP_NO_COMPRESSION
client_ctxt.load_cert_chain('../certificate.pem', '../key.pem')

with socket.socket() as s:
    s.connect((host, 2222))
    with client_ctxt.wrap_socket(s, server_hostname=host) as ssock:
        ssock.send(b'wassup dawg')
        print(ssock.version())