import os
import random
import socket
import threading
import sys


# Example bots -----------------------------------------
def alice(input, alt_action=None):
    return f"I think {input + 'ing'} sounds great!"


def bob(input, alt_action=None):
    if alt_action is None:
        return "Not sure about {}. Don't I get a choice?".format(input + "ing")
    else:
        return "Sure, both {} and {} seems ok to me.".format(input, alt_action + "ing")


def dora(input, alt_action=None):
    alternatives = ["code", "sing", "sleep", "fight"]
    alt_action = random.choice(alternatives)
    out = "Yea, {} is an option. Or we could do some {}.".format(input, alt_action + "ing")
    return out, alt_action


def chuck(input, alt_action=None):
    #action = alt_action + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]

    if action in bad_things:
        return "YES! Time for some {}!!".format(input)
    elif action in good_things:
        return "{} is so boooriiiing! I'm not doing that".format(input)
    return "I don't care!"


# -------------------------------------------------------------


# Data for configuring socket
ip = '127.0.0.1'
port = 8888

# Accepted verbs for response from bots
verbs = ["sing", "talk", "kill", "fight", "kiss", "dream", "grown"]
action = ''

# Main functions -------------------------------------------

# Connects to server and creating client information
def connect():
    global client

    # Saving client data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    client.connect((ip, port))

# Handles messages from server
def receive():
    global action, bot, upBot

    # Boolean for tracking if nickname has been asked for or not
    ##counter = False

    while True:
        # If server has already asked for nickname
        #if counter == True:
        #   print("\nWaiting for message from server...")

        try:
            # Collection message from server
            message = client.recv(1024).decode('ascii')

            # Looking for verbs in message from server
            vyes = 0
            vno = 0
            for v in verbs:
                if v in message:
                    vyes = vyes + 1
                    action = v
                else:
                    vno = vno + 1

            # String for seeing name strongly on server
            upBot = str(bot).upper()

            # If server asks for nickname
            if message == 'NICK':
                client.send(bot.encode('ascii'))
                ##counter = True
            # If the server has sent a nickname
            elif ':NEWNICKI' in message:
                message = message.replace(":NEWNICKI","")
                print(f"\n{message.upper()} joined the chat!")
            # If the user has sent a message that the server dont't want a response from bots
            elif ':HUMWRITE' in message:
                message = message.replace(':HUMWRITE', "")
                print(message)
            # If server sends message about new connected user
            elif ':CONNECT' in message:
                message = message.replace(':CONNECT', "")
                print(message)
            # If server sends message about new disconnected user
            elif ':DISCO' in message:
                message = message.replace(':DISCO', "")
                print(message)
            # If the server has sent an empty or no verbs that match
            elif vyes == 0:
                print("\nMessage from server had no matching verb!")
                client.send(f"{upBot}: No verb dude!".encode('ascii'))
            else:
                # For testing######
                print(f"\nMessage from server: {message}")

                # Bot responses to verb
                match bot:
                    case 'alice':
                        response = alice(action)
                    case 'bob':
                        response = bob(action)
                    case 'dora':
                        response, doraAction = dora(action)
                    case 'chuck':
                        response = chuck(action, )

                # Sending message to server
                send(response)
        except:
            print("Error: Couldn't process message from server!")
            client.close()
            break

# Sending message to server
def send(response):

    # Making output string from responses
    message = f'{upBot}: {response}'

    # For testing#######
    print(f"\n'Sending: {message}'")

    # Sending message to server
    client.send(message.encode('ascii'))

# Takes input from client
# This is so the program can function as a normal chat room if needed,
# but more importantly for easily closing the program without crashing
def write():
    while True:
        message = input("").lower()
        if message == "exit":
            disconnect()
        else:
            send(message+":HUMWRITE")

# Disconnects from server
def disconnect():
    client.send("exit".encode('ascii'))
    client.close()
    sys.exit()

# ----------------------------------------------------------------------


################################### Program runs from here ######################################

# Input response for name of bot (MAYBE TEMPORARY)
# Might replace for a list instead
bot = input("Name of user: ").lower()

# Connecting to the server
connect()

# Threading threads
receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()


