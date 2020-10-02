import sys, socket


def killit(sock: socket):
    sock.close()
    print("[x] Server Disconnected.")
    sys.exit()
