---

# Terminal Chat Application

## Overview

This terminal-based chat application allows multiple users to connect and communicate in real-time through a server-client model. It supports broadcasting messages, private messaging, and dynamically assigns colors and styles to users to enhance readability. The client script connects to a server, sends and receives messages, and displays them in color-coded format.

## Features

- **Real-time Messaging**: Send and receive messages instantly.
- **Private Messaging**: Send messages directly to specific users.
- **User List**: Request and display a list of currently connected users.
- **Color and Style Customization**: Each user is assigned a unique color and style for their messages.

## Getting Started

### Prerequisites

- Python 3.x
- `colorama` library (for colored terminal output)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Required Libraries:**

   ```bash
   pip install colorama
   ```

### Running the Server

1. Save the server script as `server.py`.

2. Run the server:

   ```bash
   python server.py
   ```

   The server will start listening on `0.0.0.0:5002`. Note the IP address and port for use in the client script.

### Running the Client

1. Save the client script as `client.py`.

2. Update the `SERVER_HOST` variable in `client.py` with the server’s IP address.

3. Run the client:

   ```bash
   python client.py
   ```

   Enter your name when prompted to join the chat.

### Usage

**Client Commands:**

- **Broadcast Message**: Type a message and press Enter to broadcast it to all connected users.
- **Private Message**: Use `/pm <username> <message>` to send a private message to a specific user.
- **List Users**: Use `/users` to request a list of connected users.
- **Quit**: Type `q` to disconnect from the server.

### Server Script Explanation

- **Color and Style Assignment**: Each client is assigned a unique color and style using `colorama`.
- **Message Handling**: Receives and broadcasts messages, including private messages, to all clients.
- **Error Handling**: Includes basic error handling and debug messages for tracking issues.
- **Resource Cleanup**: Ensures proper cleanup of resources when the server shuts down.

### Client Script Explanation

- **Connection**: Connects to the server using the specified IP address and port.
- **Message Formatting**: Formats messages with date-time stamps, colors, and styles.
- **Message Parsing**: Handles incoming messages and parses ANSI escape codes for color and style.

## Example

**Starting the server:**

```
[*] Listening as 0.0.0.0:5002
```

**Client connection:**

```
Enter your name:
```

**Sending a broadcast message:**

```
Hello, everyone!
```

**Sending a private message:**

```
/pm user2 Hi there!
```

**Listing users:**

```
/users
```

**Disconnecting:**

```
q
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
