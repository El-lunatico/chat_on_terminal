import socket
from threading import Thread
from colorama import Fore, Style, init
import random

# Initialize colors
init()

# Set the available colors and styles
colors = [
    Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
    Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
    Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
]

styles = [Style.DIM, Style.NORMAL, Style.BRIGHT]

used_colors = set()

separator_token = "<SEP>"
client_sockets = {}
usernames = {}

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def get_unique_color_and_style():
    available_colors = [color for color in colors if color not in used_colors]
    if not available_colors:
        return Fore.WHITE, Style.NORMAL  # Fallback if all colors are used

    color = random.choice(available_colors)
    used_colors.add(color)
    
    style = random.choice(styles)
    
    return color, style

def broadcast(message, sender_socket=None):
    for client_socket in client_sockets.values():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"[!] Error sending broadcast message: {e}")

def private_message(receiver_username, message):
    receiver_socket = client_sockets.get(receiver_username)
    if receiver_socket:
        try:
            receiver_socket.send(message.encode())
        except Exception as e:
            print(f"[!] Error sending private message to {receiver_username}: {e}")
    else:
        print(f"[!] User {receiver_username} not found.")

def handle_client(cs):
    username = None
    color, style = get_unique_color_and_style()  # Assign unique color and style
    try:
        # Initial username setup
        username = cs.recv(1024).decode()
        if username in client_sockets:
            cs.send("Username already taken. Try again.".encode())
            cs.close()
            return
        usernames[cs] = username
        client_sockets[username] = cs
        broadcast(f"{color}{style}{username} has joined the chat.{Style.RESET_ALL}")

        while True:
            msg = cs.recv(1024).decode()
            if not msg:
                break

            print(f"[DEBUG] Received message: {msg}")

            if msg.startswith("/pm "):
                parts = msg[4:].split(" ", 1)
                if len(parts) < 2:
                    cs.send("Invalid private message format. Use /pm <username> <message>".encode())
                else:
                    receiver, private_msg = parts[0], parts[1]
                    sender = usernames.get(cs, "Unknown")
                    private_message(receiver, f"{color}{style}[Private] {sender}: {private_msg}{Style.RESET_ALL}")

            elif msg == "/users":
                user_list = "Connected users: " + ", ".join(usernames.values())
                print(f"[DEBUG] Sending user list: {user_list}")
                cs.send(f"{color}{style}{user_list}{Style.RESET_ALL}".encode())
            
            else:
                # Handle regular chat messages
                msg = msg.replace(separator_token, ": ")
                broadcast(f"{color}{style}{msg}{Style.RESET_ALL}", sender_socket=cs)

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        if username:
            print(f"[DEBUG] {username} disconnected.")
            client_sockets.pop(username, None)
            broadcast(f"{color}{style}{username} has left the chat.{Style.RESET_ALL}")
        usernames.pop(cs, None)
        used_colors.discard(color)  # Free up the color when client disconnects
        cs.close()

try:
    while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        client_socket.send("Enter your username: ".encode())
        t = Thread(target=handle_client, args=(client_socket,))
        t.daemon = True
        t.start()
except KeyboardInterrupt:
    print("\n[!] Server is shutting down...")
finally:
    for cs in client_sockets.values():
        cs.close()
    s.close()
    print("[*] Server shutdown complete.")
