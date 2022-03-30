import os
import socket
import threading
import sys
import random

# List of verbs in another file
import time

# Bots in another file
import bots


# Connects to server and creating client information
def connect():
    global client, ip, port

    # Saving client data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    client.connect((ip, port))


# Bot function for when a bot is running
def bot(bprint=True):
    global upBot, client, user
    counter = 0

    # For turning off prints if specified
    if not bprint:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    while True:
        # Looking for verbs in message from server
        try:
            # Gathering message from server
            message = client.recv(1024).decode('UTF-8')

            # String for seeing name strongly on server
            upBot = str(user).upper()

            # If server asks for nickname
            if message == 'NICK':
                client.send(user.encode('UTF-8'))
            # If the server has sent a nickname
            elif ':NEWNICKI' in message:
                message = message.replace(":NEWNICKI", "")
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
                time.sleep(0.1)
            # If the message from server is empty, the client starts counting times it has been empty
            elif message == "":
                counter = counter + 1
                print(f"Waiting for server, {counter}")
                time.sleep(1)
                # If server has sent 3 empty messages, the client disconnects
                if counter == 3:
                    client.close()
                    print("Lost server, RIP")
                    sys.exit()
            else:
                # For testing
                print(f"\nMessage from server: {message}")

                response = run_bots(message)

                # Sending message to server
                send(response + ":BOT")
        except:
            print("Could not receive message from server!")
            client.close()
            break


def run_bots(action):
    global user
    # Bot responses to verb
    match user:
        case 'billy':
            return bots.billy(action)
        case 'bobby':
            return bots.bobby(action)
        case 'sarah':
            return bots.sarah(action)
        case 'chris':
            return bots.chris(action)


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
                message = message.replace(":NEWNICKI", "")
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
            # If server sends empty message, it will count each time it sends empty
            elif message == "":
                counter = counter + 1
                # If the server has sent 3 empty messages, it will disconnect
                if counter == 4:
                    client.close()
                    break
                else:
                    print(f"Waiting for server, {counter}")
                    time.sleep(1)
            else:
                print(message)
        except:
            print("Error: Couldn't process message from server!")
            client.close()
            break


# Sending message to server
def send(response):
    # If bots are sending messages, they will wait a random time between 0.1 and 1 second
    # This is to prevent print errors and to make the bots feel more human
    if isBot:
        time.sleep(random.randint(1, 10) / 10)

    # Making output string from responses
    message = f'{user.upper()}: {response}'

    # Sending message to server
    client.send(message.encode('utf-8'))

    # Prints message for user
    print(f"YOU: {response}")


# Takes input from client
# This is so the program can function as a normal chat room as well as have talking bots
def write():
    while True:
        message = input("").lower()

        # Exits shell if user specifies, else sends the message to server
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

try:
    # If user needs help with syntax
    if (sys.argv[1]) == str("-h"):
        print("Usage: python3 client.py [IP ADDRESS] [PORT] [OPTIONAL BOT NAME] [OPTIONAL VERBOSE -v]")
        print("IMPORTANT: Only supports python 3.10 and higher")
        print()
    else:
        # Data for configuring socket
        ip = sys.argv[1]
        port = int(sys.argv[2])

        # Variables used in functions that needs to be global
        client = ""
        upBot = None
        isBot = False
        verbose = False

        # Input response for name of user
        # If the client is started with a name, it is in bot mode and will launch a bot instead
        try:
            arg = sys.argv[3]
            if arg in bots.bots:
                user = arg
                isBot = True
        except:
            user = input("Name of user: ").lower()

        # If user has specified verbose bot, sets boolean
        try:
            arg = sys.argv[4]
            if arg == "-v":
                verbose = True
        except:
            verbose = False

        # Connecting to the server
        connect()

        # If client is marked as bot, starts thread in bot function. If verbose is True --> turns on prints
        # If human, starts the normal client receive function
        if isBot:
            botThread = threading.Thread(target=bot, args=(verbose,))
            botThread.start()
        else:
            # Threading threads
            receiveThread = threading.Thread(target=receive)
            receiveThread.start()

            # Starts write function in thread which is for typing.
            # If bot, the write function can be used to close the thread
            writeThread = threading.Thread(target=write)
            writeThread.start()
except:
    print("\nWrong syntax. Type -h for help!\n")

