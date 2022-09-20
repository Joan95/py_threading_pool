import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = ": "
new_user_tag_id = "new_id_username: "

# Init colors
init()

colors = [
    Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

client_name = None

# TAGS for comments
feedback_waiting_tag = f"[*]"
feedback_positive_tag = f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}]"
feedback_error_tag = f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}]"
feedback_warning_tag = f"[!!]"
feedback_input_tag = f"[>>]:"


def init_random_color():
    return random.choice(colors)


def init_socket_client():
    global client_name

    client_socket = socket.socket()

    print(f"{feedback_waiting_tag} Connecting to {SERVER_HOST}:{SERVER_PORT}...")

    try:
        # connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"{feedback_positive_tag} Connected.")
        client_name = str(input(f"{feedback_input_tag} Enter your nickname: "))
        print(f"{feedback_positive_tag} Hello {client_name}!\n")
        client_socket.send(f"{new_user_tag_id}{client_name}".encode())
    except socket.timeout as st:
        print(st)
        print(f"{feedback_warning_tag} - Server may be down")
        client_socket = None
    except ConnectionRefusedError as cre:
        print(cre)
        print(f"{feedback_error_tag} - Server may be down")
        client_socket = None
    except ConnectionError as ce:
        print(ce)
        print(f"{feedback_error_tag} - Unexpected Connection Error happened")
        client_socket = None

    return client_socket


def listen_for_messages():
    pass


def check_for_input_message():
    correct_message = False
    message = None

    while not correct_message:
        message = input(f"{feedback_input_tag} ")
        if message:
            correct_message = True
        else:
            print(f"{feedback_warning_tag} Empty messages can not be send, try again!")

    return message


def main():
    client_color = init_random_color()
    client_socket = init_socket_client()
    need_to_drop = False

    if client_socket:
        t = Thread(target=listen_for_messages)
        t.daemon = True
        t.start()

        try:
            while not need_to_drop:
                to_send = check_for_input_message()

                date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                to_send = f"{client_color} {date_now} {client_name}{separator_token}{to_send}{Fore.RESET}"
                # finally, send the message
                try:
                    client_socket.send(to_send.encode())
                except ConnectionResetError as cre:
                    print(cre)
                    print(f"{feedback_error_tag} - Server may have been closed, please reattempt the connection")
                    need_to_drop = True
        finally:
            client_socket.close()


if __name__ == "__main__":
    main()

