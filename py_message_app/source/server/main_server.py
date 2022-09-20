# https://www.thepythoncode.com/article/make-a-chat-room-application-in-python

import socket
from threading import current_thread, Semaphore, Thread
from colorama import Fore, init, Back

from MyThreadPool import ThreadPool as MyThreadPoolClass

# Server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = ": "
new_user_tag_id = "new_id_username: "

MAX_CONNECTIONS_ALLOWED = 15

# List of client sockets
client_sockets = dict()

# List of active users
active_users_dict = dict()

# Init colors
init()

# TAGS for comments
feedback_waiting_tag = f"[{Fore.LIGHTBLUE_EX}*{Fore.RESET}]"
feedback_connection_tag = f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]"
feedback_disconnection_tag = f"[{Fore.LIGHTMAGENTA_EX}-{Fore.RESET}]"
feedback_positive_tag = f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}]"
feedback_error_tag = f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}]"
feedback_warning_tag = f"[{Fore.LIGHTYELLOW_EX}!!{Fore.RESET}]"
feedback_input_tag = f"[>>{Fore.RESET}]:"


def init_server():

    # Init server
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    return server_socket


def listen_client(semaphore, thread_pool, client_socket):
    global active_users_dict

    thread_finished = False
    received_handshake = False

    try:
        while not thread_finished:
            with semaphore:
                # Call activate, it will be activated only once
                thread_pool.activate(current_thread().name)
                msg = client_socket.recv(1024).decode()
                if msg:
                    if not received_handshake:
                        # Received handshake
                        received_handshake = True
                        active_users_dict[current_thread().name] = dict({'ip': client_socket.getsockname()[0],
                                                                         'port': client_socket.getsockname()[
                                                                             1],
                                                                         'user_name': msg.replace(
                                                                             new_user_tag_id,
                                                                             ""),
                                                                         'messages_to': list()})
                    else:
                        active_users_dict[current_thread().name]['messages_to'].append(msg)
                        print(msg)
                else:
                    print("Client down.")
                    thread_finished = True
    except ConnectionResetError as cre:
        print(f"\t{feedback_warning_tag} {cre}")
    finally:
        thread_pool.deactivate(current_thread().name)
        client_sockets[current_thread().name].remove(client_socket)
        print(f"{feedback_disconnection_tag} Client {current_thread().name} got disconnected.")


def main():
    thread_pool = MyThreadPoolClass()
    semaphore = Semaphore(MAX_CONNECTIONS_ALLOWED)

    server_socket = init_server()
    print(f"{feedback_waiting_tag} Server listening as {Fore.LIGHTGREEN_EX}{SERVER_HOST}{Fore.RESET} "
          f"at port {SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"{feedback_connection_tag} New client: {client_address} connected.")

            connection_id = f"{client_socket.getsockname()[0]}:{client_socket.getsockname()[1]}"

            if connection_id in client_sockets:
                connection_id = f"{connection_id}_{list(client_sockets).count(connection_id)}"

            # Add new socket into client list
            client_sockets[connection_id] = list()
            client_sockets[connection_id].append(client_socket)

            # Create a new Thread
            client_thread = Thread(target=listen_client,
                                   name=f"{connection_id}",
                                   args=(semaphore, thread_pool, client_socket), daemon=True)

            # Start the party!
            client_thread.start()
    finally:
        server_socket.close()
        print(f"{feedback_waiting_tag} Server closed")


if __name__ == "__main__":
    main()

