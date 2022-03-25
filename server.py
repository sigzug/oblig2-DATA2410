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
        client.send(message)

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
                print(message)
                ##broadcast(message)
        except:
            disconnect(client)
            break

        action = input("\nServer: ")

        try:
            client.send(action.encode('ascii'))
        except:
            disconnect(client)
            break



def receive():
    while True:
        if len(clients) == 0:
            print("\nServer is listening...")

        # Sets up client variable and address with accept()
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Asks for nickname (TEMPORARY)
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Puts name and client inforamtion in array
        nicknames.append(nickname)
        clients.append(client)

        action = input("\nServer: ")

        # If client disconnects mid-input interrupt, server prints that to the console and moves on
        try:
            # Sends the action sentence to the client
            client.send(f'{action}'.encode('ascii'))
            ##client.send('Connected to the server'.encode('ascii'))

            # Prints information to console for logging
            print(f"\nNickname of the client is '{nickname}'")

            # Starts thread in function handle()
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        except:
            #Prints error message to console
            print(f"Client '{nickname}' has disconnected")

            # Removes client information from lists and such
            disconnect(client)

# Handling disconnecting clients
def disconnect(client):
    index = clients.index(client)
    nickname = nicknames[index]
    clients.remove(client)
    client.close()

    broadcast(f'{nickname} left the chat'.encode('ascii'))
    print(f"'{nickname}' has disconnected!")
    nicknames.remove(nickname)

    print("\nServer is listening...")


#print("Server is listening...")
receive()
