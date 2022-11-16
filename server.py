import socket
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

from util import generate_key, format_key

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER_HOST, SERVER_PORT))
    sock.listen(5)

    print(f'Running in {SERVER_HOST}:{SERVER_PORT}\n')
    print('- Wait connection...')

    client, __ = sock.accept()
    print('- Connected, performing key exchange...')

    # keys received and generated
    common = int(client.recv(1024).decode())
    secret = generate_key()
    public = common + secret

    # sending "public" key and waiting for peer's public key
    client.send(str(public).encode())
    public_peer = int(client.recv(1024).decode())
    message_secret = public_peer + secret

    print(f'- Encrypt key is: {format_key(message_secret)}\n')

    key_bytes = message_secret.to_bytes(32, byteorder='little')
    fernet = Fernet(urlsafe_b64encode(key_bytes))

    print('=' * 20)

    try:
        while True:            
            # wait response
            client_msg = client.recv(1024)
            client_msg_decrypted = fernet.decrypt(client_msg)
            print(f'client> {client_msg_decrypted.decode()}')

            message = input('message> ').strip()
            encrypted_msg = fernet.encrypt(message.encode())
            client.send(encrypted_msg)
            print('...')
    except KeyboardInterrupt:
        print('Bye.')
        sock.close()


main()
