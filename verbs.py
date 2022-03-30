
# Finding words that need different ending
def ending(word):
    if 'e' in word[-1] or 'y' in word[-1]:
        if word == 'play':
            return word + 'ing'
        word = word[:-1]
        return word + 'ing'
    else:
        return word + 'ing'


# Finding if a hello-word is in the input sentence or word
def findHello(message):
    if message in helloL:
        return True
    else:
        return False


# Finding if the message input has a verb from the verb list in it
def findVerb(message):
    # Looking for verb in message from server
    for v in verbs:
        if v in message:
            return v
    return ""


bad_verbs = ["accuse", "beat", "bite", "break", "kill", "crunch", "burn", "creep", "cry", "cut",
             "disagree", "fail", "fight", "hit",  "lie", "swear", "tear", "weep"]

good_verbs = ["achieve", "ask", "arrange", "bathe", "bake", "build", "carry", "cook", "dance", "sing",
              "discuss", "drink", "drive", "eat", "explain", "forget", "hide", "hug", "kiss", "laugh", "love",
              "read", "relax", "shake", "speak", "talk", "think", "watch", "win", "write", "play"]

verbs = bad_verbs + good_verbs

helloL = ["hello", "hi", "hey", "hei"]

hruL = ["how are you", "are you ok", "are you fine"]