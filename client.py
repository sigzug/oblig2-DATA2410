import random
import socket
import threading

# Bots
import time

bots = ["alice", "bob", "dora", "chuck"]

def alice (input, alt_action = None):
    return f"I think {input + 'ing'} sounds great!"

def bob (input, alt_action = None ):
    if alt_action is None:
        return "Not sure about {}. Don't I get a choice?".format(input + "ing")
    else:
        return "Sure, both {} and {} seems ok to me.".format(input, alt_action + "ing")

def dora (input, alt_action = None):
    alternatives = ["coding", "singing", "sleeping", "fighting"]
    alt_action = random.choice(alternatives)
    out = "Yea, {} is an option. Or we could do some {}.".format(input, alt_action + "ing")
    return out, alt_action

def chuck (input, alt_action = None):
    action = input + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]

    if action in bad_things:
        return "YES! Time for some {}!!".format(action)
    elif action in good_things:
        return "{} is so borrriiiing! I'm not doing that".format(action)
    return "I don't care!"


#nickname = random.choice(bots)

ip = '127.0.0.1'
port = 8888

# Saving client data
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to server
client.connect((ip, port))

# Socket functions
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send("Alice".encode('ascii'))
            elif message != "":
                print(message)
                output = alice(message)
                print(output)
                write(output)
            else:
                print(message)
        except:
            print("error")
            client.close()
            break

def write(input):
        message = f'Alice: {input}'
        print(f"sending... {message}")
        client.send(message.encode('ascii'))


# Threading
receiveThread = threading.Thread(target=receive)
receiveThread.start()

#writeThread = threading.Thread(target=write)
#writeThread.start()