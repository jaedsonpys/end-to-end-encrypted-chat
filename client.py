import socket
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

from util import generate_key, format_key


def main():
    host = input('Host to connect: ').strip()
    port = int(input('Port to connect: ').strip())

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    common = generate_key()
    secret = generate_key()
    public = common + secret

    # sending common key to server
    sock.send(str(common).encode())

    # getting public key from peer and sending own key
    public_peer = int(sock.recv(1024).decode())
    sock.send(str(public).encode())

    message_secret = secret + public_peer
    print(f'- Encrypt key is: {format_key(message_secret)}')

    key_bytes = message_secret.to_bytes(32, byteorder='little')
    fernet = Fernet(urlsafe_b64encode(key_bytes))


main()
