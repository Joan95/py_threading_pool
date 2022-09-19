# https://www.thepythoncode.com/article/make-a-chat-room-application-in-python

import socket
import threading
from threading import current_thread, Semaphore, Thread
from MyThreadPool import ThreadPool as MyThreadPoolClass

# Server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = ": "

MAX_CONNECTIONS_ALLOWED = 15

# List of client sockets
client_sockets = set()


def init_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    return server_socket


def listen_client(semaphore, thread_pool, client_socket):
    while True:
        try:
            with semaphore:
                # Call activate, it will be activated only once
                thread_pool.activate(threading.current_thread().name)
                msg = client_socket.recv(1024).decode()
                print(msg)
        finally:
            thread_pool.deactivate(threading.current_thread().name)


def main():
    thread_pool = MyThreadPoolClass()
    semaphore = Semaphore(MAX_CONNECTIONS_ALLOWED)
    thread_count = 0

    server_socket = init_server()
    print(f"[*] Server listening as {SERVER_HOST} at port {SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[+] Client: {client_address} connected.")
            # Add new socket into client list
            client_sockets.add(client_socket)

            # Create a new Thread
            client_thread = Thread(target=listen_client, name=f"{thread_count}",
                                   args=(semaphore, thread_pool, client_socket), daemon=True)
            thread_count += 1

            # Start the party!
            client_thread.start()
    finally:
        server_socket.close()
        print("[*] Server closed")


if __name__ == "__main__":
    main()

