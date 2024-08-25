import cv2
import socket
import pickle
import struct
import time

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(1)
print("Waiting for a connection...")
client_socket, addr = server_socket.accept()
print(f"Connected to {addr}")

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

while True:
    start_time = time.time()  # Start time for debugging
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Display the frame in a preview window
    cv2.imshow('Webcam Preview', frame)
    
    # Serialize the frame
    data = pickle.dumps(frame)
    
    # Send message length first
    message_size = struct.pack("L", len(data))
    
    # Send the frame data
    try:
        client_socket.sendall(message_size + data)
    except Exception as e:
        print(f"Error sending data: {e}")
        break

    # Print debugging information
    print(f"Frame sent, size: {len(data)} bytes, time taken: {time.time() - start_time:.2f} seconds")

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the connection
cap.release()
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
