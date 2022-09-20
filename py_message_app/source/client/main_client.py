import socket
import random
import time
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = ": "
new_user_tag_id = "new_id_username: "
reconnect_number_of_attempts = 5
time_to_wait = 5

# Init colors
init()

colors = [
    Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

dead_server = False

# TAGS for comments
feedback_waiting_tag = f"[{Fore.LIGHTBLUE_EX}*{Fore.RESET}]"
feedback_positive_tag = f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}]"
feedback_error_tag = f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}]"
feedback_warning_tag = f"[{Fore.LIGHTYELLOW_EX}!!{Fore.RESET}]"
feedback_input_tag = f"[{Fore.YELLOW}>>{Fore.RESET}]"


def init_random_color():
    return random.choice(colors)


def init_socket_client():
    client_socket = socket.socket()
    print(f"{feedback_waiting_tag} Connecting to SERVER...")

    try:
        # connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"{feedback_positive_tag} Connected successfully!")
    except socket.timeout as st:
        print(f"\t{feedback_error_tag} {st}")
        print(f"\t{feedback_warning_tag} - Server currently unavailable")
        client_socket = None
    except ConnectionRefusedError as cre:
        print(f"\t{feedback_error_tag} {cre}")
        print(f"\t{feedback_warning_tag} - Server may be down")
        client_socket = None
    except ConnectionError as ce:
        print(ce)
        print(f"\t{feedback_error_tag} - Unexpected Connection Error happened")
        client_socket = None

    return client_socket


def ask_for_login_name(client_socket):
    global dead_server

    print(f"{feedback_input_tag} Enter your nickname: ")
    client_name = str(input("\t"))
    print(f"{feedback_positive_tag} Hello {client_name}!\n")

    try:
        client_socket.send(f"{new_user_tag_id}{client_name}".encode())
    except ConnectionResetError as cre:
        print(cre)
        dead_server = True

    return client_name


def listen_for_messages(client_socket):
    global dead_server
    try:
        while True:
            msg = client_socket.recv(1024).decode()
            print(msg)
    except ConnectionResetError as cre:
        print(cre)
        dead_server = True


def check_for_input_message():
    global dead_server

    correct_message = False
    message = None
    send_message = True

    while not correct_message:
        message = input(">> ")

        if message:
            correct_message = True
        else:
            print(f"{feedback_warning_tag} Empty messages can not be send, try again!")

        if dead_server:
            send_message = False
            message = None
            break

    return message, send_message


def main():
    global dead_server

    client_color = init_random_color()
    client_socket = init_socket_client()
    need_to_drop = False
    reattempt_counter = 0

    if client_socket:
        t = Thread(target=listen_for_messages, args=(client_socket,), daemon=True)
        t.start()

        client_name = ask_for_login_name(client_socket)
        should_be_send = True

        try:
            while not need_to_drop:
                # There is connection, restart counter
                reattempt_counter = 0

                if not dead_server:
                    message, should_be_send = check_for_input_message()

                    if should_be_send:
                        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        message = f"{client_color} {date_now} {client_name}{separator_token}{message}{Fore.RESET}"
                        # finally, send the message
                        try:
                            client_socket.send(message.encode())
                        except ConnectionResetError as cre:
                            print(cre)
                            print(f"{feedback_error_tag} - Server may have been closed, please reattempt the connection")
                            need_to_drop = True

                # If server is currently down, just send following
                while dead_server and reattempt_counter < reconnect_number_of_attempts:
                    need_to_drop = True
                    reattempt_counter += 1

                    # Reattempt connection (?)
                    print(f"{feedback_waiting_tag} Reattempting connection... "
                          f"Attempt {reattempt_counter}/{reconnect_number_of_attempts}")

                    client_socket = init_socket_client()
                    if client_socket:
                        need_to_drop = False
                        dead_server = False
                        print(f"{feedback_positive_tag} Reconnected as {client_name}!")
                        client_socket.send(f"{new_user_tag_id}{client_name}".encode())

                        t = Thread(target=listen_for_messages, args=(client_socket,), daemon=True)
                        t.start()
                        break

                    if reattempt_counter < reconnect_number_of_attempts:
                        print(f"\t{feedback_waiting_tag} Trying again after {time_to_wait} seconds")
                        time.sleep(time_to_wait)
        finally:
            try:
                print(f"{feedback_positive_tag} Connection finally closed")
                client_socket.close()
            except AttributeError:
                pass


if __name__ == "__main__":
    main()

