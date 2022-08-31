# https://www.thepythoncode.com/article/make-a-chat-room-application-in-python

import socket
from threading import Thread
from MyThreadPool import ThreadPool

# Server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = ": "

# List of client sockets
client_sockets = set()


def init_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    return server_socket


def listen_client(client_socket):

    while True:
        msg = client_socket.recv(1024).decode()
        print(msg)


def main():
    server_socket = init_server()
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[+] {client_address} connected.")
            # Add new socket into client list
            client_sockets.add(client_socket)

            # Create a new Thread
            client_thread = Thread(target=listen_client, args=(client_socket,))

            # Make thread as Daemon so it ends when main finishes
            client_thread.daemon = True

            # Start the party!
            client_thread.start()
    finally:
        server_socket.close()
        print("[*] Server closed")


if __name__ == "__main__":
    main()

