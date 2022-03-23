import random
import socket
import threading

# Accepted verbs for response from bots
verbs = ["sing"]

# Example bots -----------------------------------------
def alice (input, alt_action = None):
    return f"I think {input + 'ing'} sounds great!"

def bob (input, alt_action = None ):
    if alt_action is None:
        return "Not sure about {}. Don't I get a choice?".format(input + "ing")
    else:
        return "Sure, both {} and {} seems ok to me.".format(input, alt_action + "ing")

def dora (input, alt_action = None):
    alternatives = ["code", "sing", "sleep", "fight"]
    alt_action = random.choice(alternatives)
    out = "Yea, {} is an option. Or we could do some {}.".format(input, alt_action + "ing")
    return out, alt_action

def chuck (input, alt_action = None):
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

# Saving client data
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to server
client.connect((ip, port))

# Socket functions -------------------------------------------

def receive():
    global alice, bob, dora, chuck
    while True:
        try:

            # Collection message from server
            message = client.recv(1024).decode('ascii')

            # If server asks for name (TEMPORARY)
            if message == 'NICK':
                client.send('bots'.encode('ascii'))
            else:
                print(message)

                # Looking for verb in message input
                for v in verbs:
                    if v in message:
                        action = v
                    else:
                        print("No word!")
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
            print("error")
            client.close()
            break

def write(input):
    global bot
    message = f'{input}'
    print(f"\nSending: \n{message}")
    client.send(message.encode('ascii'))


# Threading threads
receiveThread = threading.Thread(target=receive)
receiveThread.start()

#writeThread = threading.Thread(target=write)
#writeThread.start()