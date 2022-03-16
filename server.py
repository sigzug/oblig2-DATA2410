import threading
import socket

host = '127.0.0.1'  # localhost
port = 8181

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # Connected user gets accepted and address is sent to server terminal
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Asking new client for nickname
        client.send('NICK'.encode('ascii'))
        nicknames = client.recv(1024).decode('ascii')
        clients.append(client)

        # Send messages to users of network of new user
        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nicknames} joined the chat!".encode('ascii'))
        client.send("Connected to the server!".encode('ascii'))

        # Creating thread so users can be handles "simultaneously"
        thread = threading.Thread(target=handle(), args=(client,))
        thread.start()

# Running function
print("Server is listening...")
receive()