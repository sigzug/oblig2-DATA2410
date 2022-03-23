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
actions = ["Why don't we sing?"] #["work", "play", "eat", "cry", "sleep", "fight"]

# Broadcasts message to all clients in clients list
def broadcast(message):
    for client in clients:
        client.send(message)

# Handles input from clients
def handle(client):
    while True:
        try:
            # Picks up message from client and prints to console
            message = client.recv(1024).decode('ascii')
            print(message)
            ##broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break



def receive():
    while True:

        # Sets up client variable and address with accept()
        client, address = server.accept()-
        print(f"Connected with {str(address)}")

        # Asks for nickname (TEMPORARY)
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Puts name and client inforamtion in array
        nicknames.append(nickname)
        clients.append(client)

        # Picks a random action from a list with sentences (TEMPORARY)
        # PUT INPUT HERE WHEN WORKING!!
        action = random.choice(actions)

        # Prints information to console for logging
        print(f'Nickname of the client is {nickname}')
        print(f'Do you guys want to {action}')

        # Sends the action sentence to the client
        client.send(f'{action}'.encode('ascii'))
        ##client.send('Connected to the server'.encode('ascii'))

        # Starts thread in function handle()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()
