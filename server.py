import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Host = "127.0.0.1"
Port = 7000

server.bind((Host, Port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(2048)
        
            print(f"{nicknames[clients.index(client)]} sent: {message.decode('utf-8')}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat room".encode('utf-8'))
            break


def receive():
    while True:
        client, address = server.accept()

        client.send("Enter your nickname: ".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)
        broadcast(f"{nickname} joined the chat room".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
