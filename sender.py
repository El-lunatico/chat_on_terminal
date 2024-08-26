import cv2
import socket
import pickle
import struct
import time
import numpy as np

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(1)
print("Waiting for a connection...")
client_socket, addr = server_socket.accept()
print(f"Connected to {addr}")

# Open a connection to the webcam
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()
prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_frame_gray_blurred = cv2.GaussianBlur(prev_frame_gray, (5, 5), 0)

while True:
    start_time = time.time()  # Start time for debugging
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert current frame to grayscale and apply Gaussian blur
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray_blurred = cv2.GaussianBlur(frame_gray, (5, 5), 0)

    # Compute the absolute difference between the current frame and the previous frame
    frame_diff = np.abs(frame_gray_blurred.astype(np.int16) - prev_frame_gray_blurred.astype(np.int16))

    # Count the number of pixels with a significant change
    num_changed_pixels = np.sum(frame_diff > 30)

    # Check if a significant portion of the frame has changed (e.g., 5% of the total pixels)
    significant_change = num_changed_pixels > (frame_diff.size * 0.05)

    if significant_change:
        # Serialize the frame
        data = pickle.dumps(frame)
        
        # Send message length first
        message_size = struct.pack("L", len(data))

        try:
            client_socket.sendall(message_size + data)
        except Exception as e:
            print(f"Error sending data: {e}")
            break

        # Print debugging information
        print(f"Frame sent, size: {len(data)} bytes, time taken: {time.time() - start_time:.2f} seconds")
    
    # Update the previous frame to the current frame for the next iteration
    prev_frame_gray_blurred = frame_gray_blurred

    # Display the original frame in a preview window
    cv2.imshow('Webcam Preview', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the connection
cap.release()
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
