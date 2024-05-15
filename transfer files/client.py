import socket

# Function to send file to server
def send_file(connection, filename):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            connection.sendall(data)
    print(f"File '{filename}' sent successfully.")

# Client configuration
SERVER_HOST = '127.0.0.1'  # Server's IP address
SERVER_PORT = 12345        # Server's port number
BUFFER_SIZE = 1024

# Prompt user for filename
filename = input("Enter the filename to send: ")

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server.")

    # Send filename to server
    client_socket.sendall(filename.encode())

    # Send file data to server
    send_file(client_socket, filename)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    client_socket.close()

#C:\Data\second_term\network_test\Pin Pong\Server.py
#C:\Data\second_term\network_test\Pin Pong\Client.py