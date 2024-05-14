import socket
import tkinter as tk
from tkinter import filedialog

# Function to send file to server
def send_file(connection, filename):
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            connection.sendall(data)
    print(f"File '{filename}' sent successfully.")

# Function to handle file selection
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    filename = filedialog.askopenfilename()  # Open file dialog
    return filename

# Client configuration
SERVER_HOST = '127.0.0.1'  # Server's IP address
SERVER_PORT = 12345        # Server's port number
BUFFER_SIZE = 1024

try:
    # Prompt user to select file
    filename = select_file()

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server.")

    # Extract file name from the file path
    filename = filename.split("/")[-1]

    # Send filename to server
    client_socket.sendall(filename.encode())

    # Send file data to server
    send_file(client_socket, filename)

except FileNotFoundError:
    print("No file selected.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    client_socket.close()
