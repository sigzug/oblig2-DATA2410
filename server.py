import subprocess
import sys
import time
import threading
import socket
import bots


# Broadcasts message to all clients in clients list
def broadcast(message):
    for c in clients:
        send(message, c)


# Sends message to all clients except the one who sent the message
def send_rest(message, in_client):
    for c in clients:
        if c == in_client:
            # Nothing is happening
            z = 0
        else:
            send(message, c)


# Function for encoding and sending message to a client
def send(message, c):
    c.send(message.encode('utf-8'))


# Handles input from clients
def handle(in_client):
    counter = 0
    while True:
        # Picks up message from client
        try:
            message = in_client.recv(1024).decode('utf-8')

            # If the user specifies exiting
            if message == "exit":
                disconnect(in_client)
                break
            # If server lost connection to client, it will receive blank strings
            elif message == '':
                counter = counter + 1
                # Wait 3 seconds, if still no connection -> disconnect client
                if counter == 4:
                    disconnect(in_client)
                    break
                else:
                    print(f"Waiting for user, {counter}")
                    time.sleep(1)
            else:
                # Sending message to all other clients then its sender
                send_rest(message, in_client)
                print(message)
        except:
            disconnect(in_client)
            break


# Receiving new clients
def receive():
    global client
    while True:
        # Shows something on screen if there's no one connected
        if len(clients) == 0:
            print("\nServer is listening...")

        try:
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
            send_rest(nickname + ':NEWNICKI', client)

            # Starts a thread for each  client, so they can run in parallel
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            quit()
            break


# Sending new messages for all clients
def actions():
    while True:
        global processes

        # Gathering the action the server is going to send to the clients
        action = input().lower()

        # Closing server is server sends 'exit' command
        if action == 'exit':
            server.close()
            try:
                # Closes all subprocesses and server if there is any
                for p in processes:
                    p.kill()
            except:
                # Nothing is happening
                x = 0
            quit()
            sys.exit()
        # Sends server message to all clients
        else:
            broadcast(action)
            print("")


# Handling disconnecting clients
def disconnect(in_client):
    index = clients.index(in_client)
    nickname = nicknames[index]
    in_client.close()
    clients.remove(in_client)

    broadcast(f"\n{nickname.upper()} has left the chat!:DISCO")
    print(f"\n'{nickname}' has disconnected!")
    nicknames.remove(nickname)


#################### PROGRAM RUNS FROM HERE ################################
# Checks if the user has sent in any arguments from console
try:
    # If the first argument is "-h", help message is printed
    if sys.argv[1] == str("-h"):
        print("Usage: python3 server.py [PORT] [OPTIONAL BOTS -b] [OPTIONAL VERBOSE BOTS -v]")
        print("IMPORTANT: Only supports python 3.10 and higher")
        print()
    else:
        # Server network information
        # Gets port from argument in console
        host = '127.0.0.1'
        port = int(sys.argv[1])
        client = ''

        # Setting up socket and binds to ip and port. Sets the socket in listen()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        # Lists for clients and nicknames
        clients = []
        nicknames = []
        processes = []

        # Starting a thread for taking input
        actionsThread = threading.Thread(target=actions)
        actionsThread.start()

        # If user specifies v for verbose bots, sets boolean
        try:
            try:
                # If user wants all comments prints
                if sys.argv[3] == "-v":
                    verbose = True
                else:
                    verbose = False
            except:
                verbose = False


            # Starting all bots as clients if user has specified
            if sys.argv[2] == '-b':
                i = 0
                for b in bots.bots:
                    var = f"proc{i}"

                    # Saving to list for closing later
                    processes.append(var)

                    # If user had specifies verbose bots
                    if verbose:
                        processes[i] = subprocess.Popen(["python3", ".\client.py", f"{b}", "-v"])
                    else:
                        processes[i] = subprocess.Popen(["python3", ".\client.py", f"{b}"])
                    i = i + 1

            receive()
        except:
            # Receiving new clients
            receive()
# If no arguments, send wrong syntax message
except:
    print("\nWrong syntax. Type -h for help!\n")
