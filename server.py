import time
import threading
import socket
import sys

# Broadcasts message to all clients in clients list
def broadcast(message):
    for client in clients:
        send(message, client)


# Sends message to all cleints except the one who sent the message
def sendRest(message, client):
    for c in clients:
        if c == client:
            ####Nothing is happening
            z = 0
        else:
            send(message, c)


# Function for encoding and sending message to a client
def send(message, client):
    client.send(message.encode('utf-8'))

# Handles input from clients
def handle(client):
    counter = 0
    while True:
        # Picks up message from client
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "exit":
                disconnect(client)
                break
            elif counter == 3:
                disconnect(client)
                break
            elif message == '':
                counter = counter + 1
                print(f"Waiting for user, {counter}")
                time.sleep(1)
            else:
                sendRest(message, client)
                print(message)
        except:
            disconnect(client)
            break


# Receiving new clients
def receive():
    while True:

        # Shows something on screen if there's no one connected
        if len(clients) == 0:
            print("\nServer is listening...")

        # Sets up client variable and address with accept()
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Asks for nickname
        send('NICK', client)
        nickname = client.recv(1024).decode('utf-8')

        # Puts name and client information in array
        nicknames.append(nickname)
        clients.append(client)

        # Prints information to console for logging
        print(f"{nickname} joined the chat!")
        send("Connected to server!:CONNECT", client)
        sendRest(nickname + ':NEWNICKI', client)

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
    client.close()
    clients.remove(client)

    broadcast(f"\n{nickname.upper()} has left the chat!:DISCO")
    print(f"\n'{nickname}' has disconnected!")
    nicknames.remove(nickname)


#################### PROGRAM RUNS FROM HERE ################################
# Checks if the user has sent in any arguments from console
try:
    # If the first argument is "-h", help message is printed
    if sys.argv[1] == str("-h"):
        print("Usage: python3 server.py [PORT]")
        print("IMPORTANT: Only supports python 3.10 and higher")
        print()
    else:
        # Server network information
        # Gets port from argument in console
        host = '127.0.0.1'
        port = 8888 #int(sys.argv[1])

        # Setting up socket and binds to ip and port. Sets the socket in listen()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        # Lists for clients and nicknames
        clients = []
        nicknames = []

        # Starting a thread for taking input
        actionsThread = threading.Thread(target=actions)
        actionsThread.start()

        # Receiving new clients
        receive()
        # If no arguments, send wrong syntax message
except:
    print("\nWrong syntax. Type -h for help!\n")
