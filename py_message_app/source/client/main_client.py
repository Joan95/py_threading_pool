import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = ": "

# Init colors
init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]
client_color = None
client_socket = None
client_name = None


def init_client():
    global client_color, client_socket, client_name

    client_color = random.choice(colors)
    client_socket = socket.socket()

    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    # connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")
    client_name = input("Enter your nickname: ")
    print(f"[>] Hello {client_name}!\n")


def listen_for_messages():
    pass


def main():
    init_client()

    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()

    while True:
        to_send = input(">> ")

        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}] {client_name}{separator_token}{to_send}{Fore.RESET}"
        # finally, send the message
        client_socket.send(to_send.encode())


if __name__ == "__main__":
    main()

