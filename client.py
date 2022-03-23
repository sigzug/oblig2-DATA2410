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
bot = ''

# Accepted verbs for response from bots
verbs = ["sing", "talk", "kill", "fight", "kiss", "dream", "grown"]

# Main functions -------------------------------------------
def connect():
    global client

    # Saving client data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    client.connect((ip, port))

def receive():
    global alice, action, bob, dora, chuck

    # Boolean for tracking if nickname has been asked or not
    counter = False

    while True:
        if counter == True:
            print("\nWaiting for message from server...")

        try:
            # Collection message from server
            message = client.recv(1024).decode('ascii')

            # If server asks for name (TEMPORARY)
            if message == 'NICK':
                client.send('bots'.encode('ascii'))
                counter = True
            elif message == "":
                print("\nMessage from server was empty!")
            else:
                print(f"\nMessage from server: {message}")

                # Looking for verb in message input
                vyes = 0
                vno = 0
                for v in verbs:
                    if v in message:
                        vyes = vyes + 1
                        action = v
                    else:
                        vno = vno + 1

                # If no verbs that match, disconnect and restart shell
                if vyes == 0:
                    print("No verbs that match. Restarting!")
                    client.send("exit".encode('ascii'))
                    os.system('python client.py')
                    break

                # Bot responses to verb
                alice = alice(action)
                bob = bob(action)
                dora, doraAction = dora(action)
                chuck = chuck(action, doraAction)

                # Making output string from responses
                output = f'Alice: {alice}\nBob: {bob}\nDora: {dora}\nChuck: {chuck}'

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

# Connecting to the server
connect()

# Threading threads
receiveThread = threading.Thread(target=receive)
receiveThread.start()
##writeThread = threading.Thread(target=write)
##writeThread.start()



