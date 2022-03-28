import random
import socket
import threading
import sys
# List of verbs in another file
import time

import verbs
# Bots in another file
import bots


# Connects to server and creating client information
def connect():
    global client

    # Saving client data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    client.connect((ip, port))

# Bot function for when a bot is running
def bot():
    global action, upBot, client
    counter = 0
    response = ""
    while True:
        # Looking for verbs in message from server
        try:
            # Gathering message from server
            message = client.recv(1024).decode('UTF-8')

            # String for seeing name strongly on server
            upBot = str(user).upper()

            # Looking for verb in message from server
            vyes = 0
            vno = 0
            for v in verbs.verbs:
                if v in message:
                    vyes = vyes + 1
                    action = v
                else:
                    vno = vno + 1

            # If server asks for nickname
            if message == 'NICK':
                client.send(user.encode('UTF-8'))
            # If the server has sent a nickname
            elif ':NEWNICKI' in message:
                message = message.replace(":NEWNICKI","")
                print(f"\n{message.upper()} joined the chat!")
            # If server sends message about new connected user
            elif ':CONNECT' in message:
                message = message.replace(':CONNECT', "")
                print(message)
            # If server sends message about new disconnected user
            elif ':DISCO' in message:
                message = message.replace(':DISCO', "")
                print(message)
            # If a bot has sent something this bot will just ignore
            elif ':BOT' in message:
                ###NOTHING
                x = 0
            # If server has sent 3 empty messages, the client disconnects
            elif counter == 3:
                client.close()
                print("Lost server, RIP")
                sys.exit()
            # If the message from server is empty, the client starts counting times it has been empty
            elif message == "":
                counter = counter + 1
                print(f"Waiting for server, {counter}")
                time.sleep(1)
            # If the server has sent an empty or no verbs that match
            elif vyes == 0:
                print("\nMessage from server had no matching verb!")
                client.send(f"{upBot}: No verb dude!:BOT".encode('utf-8'))
            else:
                # For testing##
                print(f"\nMessage from server: {message}")

                # Bot responses to verb
                match user:
                    case 'alice':
                        response = bots.alice(action)
                    case 'bob':
                        response = bots.bob(action)
                    case 'dora':
                        response, alt = bots.dora(action)
                    case 'chuck':
                        response = bots.chuck(action,)
                    case 'billy':
                        response, alt = bots.billy(action)
                    case 'bobby':
                        response = bots.bobby(action,)

                # Sending message to server
                send(response + ":BOT")
        except:
            print("Could not receive message from server!")
            client.close()
            break


# Handles messages from server
def receive():
    counter = 0
    while True:
        try:
            # Collection message from server
            message = client.recv(1024).decode('utf-8')

            # If server asks for nickname
            if message == 'NICK':
                client.send(user.encode('utf-8'))
            # If the server has sent a nickname
            elif ':NEWNICKI' in message:
                message = message.replace(":NEWNICKI","")
                print(f"\n{message.upper()} joined the chat!")
            # If server sends message about new connected user
            elif ':CONNECT' in message:
                message = message.replace(':CONNECT', "")
                print("\n"+message)
            # If server sends message about new disconnected user
            elif ':DISCO' in message:
                message = message.replace(':DISCO', "")
                print(message)
            # If a bot send a message is will replace the word and make it standard
            elif ':BOT' in message:
                message = message.replace(":BOT", "")
                print(message)
            # If the server has sent 3 empty messages, it will disconnect
            elif counter == 3:
                client.close()
                print("Lost server, RIP")
                break
            # If server sends empty message, it will count each time it sends empty
            elif message == "":
                time.sleep(1)
                counter = counter + 1
                print(f"Waiting for server, {counter}")
            else:
                print(message)
        except:
            print("Error: Couldn't process message from server!")
            client.close()
            break

# Sending message to server
def send(response):
    # Making output string from responses
    message = f'{user.upper()}: {response}'

    # Sending message to server
    client.send(message.encode('utf-8'))

    print(f"YOU: {response}")

# Takes input from client
# This is so the program can function as a normal chat room if needed,
# but more importantly for easily closing the program without crashing
def write():
    while True:
        message = input("").lower()
        if message == "exit":
            disconnect()
        else:
            try:
                send(message)
            except:
                client.close()
                break

# Disconnects from server
def disconnect():
    client.send("exit".encode('utf-8'))
    client.close()
    sys.exit()

# ----------------------------------------------------------------------


################################### Program runs from here ######################################

# Data for configuring socket
ip = '127.0.0.1'
port = 8888

action = None

upBot = None

isBot = False

# Input response for name of bot (MAYBE TEMPORARY)
# Might replace for a list instead
user = input("Name of user: ").lower()

if user in bots.bots:
    isBot = True

# Connecting to the server
connect()

if isBot:
    botThread = threading.Thread(target=bot)
    botThread.start()
else:
    # Threading threads
    receiveThread = threading.Thread(target=receive)
    receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()


