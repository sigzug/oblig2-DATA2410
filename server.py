import os
import random
import threading
import socket

# Server network information
host = '127.0.0.1'
port = 8888

# Setting up socket and binds to ip and port. Sets the socket in listen()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists for clients and nicknames
clients = []
nicknames = []

# (TEMPORARY) List of sentences. JUST FOR TESTING
#actions = ["Why don't we sing?"] #["work", "play", "eat", "cry", "sleep", "fight"]

# Broadcasts message to all clients in clients list
def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))

# Handles input from clients
def handle(client):
    while True:
        # Picks up message from client and prints to console
        try:
            message = client.recv(1024).decode('ascii')

            if message == "exit":
                disconnect(client)
                break
            else:
                print(f"{message}")
        except:
            disconnect(client)
            break

# Receiving new clients
def receive():
    while True:
        if len(clients) == 0:
            print("\nServer is listening...")

        # Sets up client variable and address with accept()
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Asks for nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Puts name and client inforamtion in array
        nicknames.append(nickname)
        clients.append(client)

        # Prints information to console for logging
        print(f"{nickname} joined the chat!")
        broadcast(f"NEWNICKI:{nickname}")

        # Starts a thread for each  client, so they can run in parallel
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Sending new messages for all clients
def actions():
    while True:
        global action
        # Gathering the action the server is going to send to the clients
        action = input().lower()
        broadcast(action)
        print("")

# Handling disconnecting clients
def disconnect(client):
    index = clients.index(client)
    nickname = nicknames[index]
    clients.remove(client)
    client.close()

    ##broadcast(f'{nickname} left the chat'.encode('ascii'))
    print(f"\n'{nickname}' has disconnected!")
    nicknames.remove(nickname)

# Starting a thread for taking input
actionsThread = threading.Thread(target=actions)
actionsThread.start()

# Receiving new clients
receive()
