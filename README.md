---

# One-Way Video Call Application

This project demonstrates a simple one-way video call using Python, OpenCV, and sockets. In this setup, the sender streams video from their webcam to the receiver in real-time.

## Prerequisites

Make sure you have Python installed along with the required libraries:

- Python 3.x
- OpenCV (`cv2`)
- `pickle` (comes with Python's standard library)
- `struct` (comes with Python's standard library)
- `socket` (comes with Python's standard library)

You can install OpenCV using pip:

```bash
pip install opencv-python
```

## How It Works

The application consists of two scripts:

1. **Sender Code:** Captures video frames from the sender's webcam, serializes the frames, and sends them over a network socket to the receiver.
2. **Receiver Code:** Receives the serialized video frames over the network, deserializes them, and displays them on the receiver's screen.

## Running the Application

### Step 1: Run the Sender

1. On the sender's machine, ensure you have the `sender.py` script ready.
2. Run the `sender.py` script. It will wait for a connection from the receiver.

### Step 2: Run the Receiver

1. On the receiver's machine, ensure you have the `receiver.py` script ready.
2. Run the `receiver.py` script. It will connect to the sender and start receiving the video stream.

### Step 3: Interact with the Application

- The video stream will be displayed on the receiver's screen.
- The sender can stop the video stream by pressing the `q` key.

## Notes

- Ensure that the receiver's IP address is correctly set in the receiver script.
- Both the sender and receiver must be on the same network or properly configured for remote connection.

## Troubleshooting

- If the connection fails, check your firewall settings and ensure that the correct IP address and port are used.
- If you experience lag or dropped frames, consider adjusting the network quality or frame size.

---
