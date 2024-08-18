import socket
from threading import Thread
from datetime import datetime
from colorama import Fore, Style, init
import random

# Initialize colors and styles
init()

# Set the available foreground colors and styles
colors = [
    Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
    Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
    Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
]

styles = [Style.DIM, Style.NORMAL, Style.BRIGHT]

# Choose a random color and style for the client
client_color = random.choice(colors)
client_style = random.choice(styles)

# Server's IP address and port
SERVER_HOST = "ues you local ip "
SERVER_PORT = 5002
separator_token = "<SEP>"

# Initialize TCP socket
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# Prompt the client for a name
name = input("Enter your name: ")
s.send(name.encode())

def parse_message(message):
    # Parse style from the message (assuming no background colors)
    if message.startswith("\x1b["):
        # Extract ANSI escape codes for color and style
        style_end = message.find("m") + 1
        style_code = message[2:style_end]
        
        message = message[style_end:]  # Extract the actual message
        
        return f"\x1b[{style_code}:-{message}{Style.RESET_ALL}"
    return message

def listen_for_messages():
    while True:
        try:
            message = s.recv(1024).decode()
            if not message:
                break
            formatted_message = parse_message(message)
            print("\n" + formatted_message)
        except Exception as e:
            print(f"[!] Error receiving message: {e}")
            break

# Start a thread to listen for incoming messages
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()
    
    if to_send.lower() == 'q':
        break
    
    elif to_send == '/users':
        s.send(to_send.encode())
    
    elif to_send.startswith('/pm '):
        s.send(to_send.encode())
    
    else:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{client_style}{client_color}[{date_now}] {name}{separator_token}{to_send}{Style.RESET_ALL}"
        s.send(to_send.encode())

# Close the socket
s.close()
