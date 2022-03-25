import os
import random
import socket
import threading


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
    action = alt_action + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]

    if action in bad_things:
        return "YES! Time for some {}!!".format(action)
    elif action in good_things:
        return "{} is so boooriiiing! I'm not doing that".format(action)
    return "I don't care!"


# -------------------------------------------------------------


# Data for configuring socket
ip = '127.0.0.1'
port = 8888

# Accepted verbs for response from bots
verbs = ["sing", "talk", "kill", "fight", "kiss", "dream", "grown"]
action = ''

# Main functions -------------------------------------------
def connect():
    global client

    # Saving client data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    client.connect((ip, port))

def receive():
    global action, bot

    # Boolean for tracking if nickname has been asked or not
    counter = False

    while True:
        # If server has already asked for nickname
        #if counter == True:
        #    print("\nWaiting for message from server...")

        try:
            # Collection message from server
            message = client.recv(1024).decode('ascii')

            # Looking for verbs in message from server
            vyes = 0
            vno = 0
            newnick = False
            for v in verbs:
                if v in message:
                    vyes = vyes + 1
                    action = v
                # I use this loop to also check if the server is broadcasting a nickname
                elif 'NEWNICKI' in message:
                    newnick = True
                else:
                    vno = vno + 1

            # String for seeing name on server
            upBot = str(bot).upper()

            # If server asks for nickname
            if message == 'NICK':
                client.send(bot.encode('ascii'))
                counter = True
            # If the server has sent a nickname
            elif newnick is True:
                nick = message.replace("NEWNICKI:","")
                nick = nick.upper()
                print(f"\n{nick} joined the chat!")
            # If the server has sent an empty or no verbs that match
            elif message == "" or vyes == 0:
                print("\nMessage from server was empty or had no verb!")
                client.send(f"{upBot}: No verb dude!".encode('ascii'))
            else:
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

                # Making output string from responses
                output = f'{upBot}: {response}'

                # Sending message to server
                write(output)
        except:
            print("Error: Couldn't process message from server!")
            client.close()
            break

# Sending message to server
def write(input):
    global bot
    message = f'{input}'
    print(f"\nSending: \n{message}")
    client.send(message.encode('ascii'))

# ----------------------------------------------------------------------


################################### Program runs from here ######################################

# Input response for name of bot (MAYBE TEMPORARY)
# Might replace for a list instead
bot = input("Name of bot: ").lower()

# Connecting to the server
connect()

# Threading threads
receiveThread = threading.Thread(target=receive)
receiveThread.start()


