import socket
import time

HOST = '192.168.50.251'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Set a timeout for the accept
s.settimeout(10)  # Timeout after 10 second

while True:
    try:
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data)
    except socket.timeout:
        # Handle timeout, for example, you can just continue to the next loop iteration
        print("Waiting for connection...")
        time.sleep(1)  # Optionally, add a small delay to prevent busy waiting
    except KeyboardInterrupt:
        print("Server interrupted. Exiting...")
        break