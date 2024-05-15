import socket
import os

# Function to receive file from client
# Function to receive file from client
# Function to receive file from client
def receive_file(connection, filename):
    directory = r'C:\Data\second_term\network_test\transfer files\recieved_files'  # Specify the directory path
    filename = os.path.basename(filename)  # Extract filename from the received filepath
    file_path = os.path.join(directory, filename)
    with open(file_path, 'wb') as f: #write binary
        while True:
            data = connection.recv(1024)
            if not data:
                break
            f.write(data)
    print(f"File '{filename}' received and saved successfully.")



# Server configuration
HOST = '127.0.0.1'  # Loopback address
PORT = 12345        # Port to listen on
BUFFER_SIZE = 1024

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening for incoming connections...")

while True:
    # Accept incoming connection
    connection, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    try:
        # Receive filename from client
        filename = connection.recv(BUFFER_SIZE).decode()
        if not filename:
            print("Invalid filename received.")
            continue

        # Receive and save file data
        receive_file(connection, filename)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        connection.close()
