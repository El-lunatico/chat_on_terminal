import cv2
import socket
import pickle
import struct
import time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8080))

while True:
    start_time = time.time()  # Start time for debugging
    
    # Receive message length first
    try:
        message_size = struct.unpack("L", client_socket.recv(struct.calcsize("L")))[0]
    except Exception as e:
        print(f"Error receiving message size: {e}")
        break
    
    # Receive the frame data
    data = b''
    while len(data) < message_size:
        try:
            packet = client_socket.recv(message_size - len(data))
            if not packet:
                break
            data += packet
        except Exception as e:
            print(f"Error receiving data: {e}")
            break
    
    # Deserialize the frame
    try:
        frame = pickle.loads(data)
    except Exception as e:
        print(f"Error deserializing data: {e}")
        break
    
    # Display the frame
    cv2.imshow('Received Video', frame)
    
    # Print debugging information
    print(f"Frame received, size: {len(data)} bytes, time taken: {time.time() - start_time:.2f} seconds")

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the connection
client_socket.close()
cv2.destroyAllWindows()