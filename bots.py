import random
import verbs

bots = ["bobby", "billy", "sarah", "chris"]


# All bots are taking in a sentence from the server and checking first if message has a hello-word.
# Then they will chekc if there is a verb in the message. If not, they will respons being confused.
# If there was a verb in the message they will respond to the word.
def billy(a):
    for w in a.split():
        if verbs.findHello(w) and len(a.split()) < 3:
            return "Hello hello! nice seeing ya!"
    if verbs.findVerb(a) == "":
        return "Man, I had a though time reading that line there!"
    else:
        a = verbs.findVerb(a)
        a_out = verbs.ending(a)
        alt = random.choice(verbs.verbs)
        alt_out = verbs.ending(alt)
        return f"{a_out} sounds super duper cool, boy! Maybe even {alt_out} would be just as fun!"


def bobby(a):
    for w in a.split():
        if verbs.findHello(w) and len(a.split()) < 3:
            return "Heiyo there!"
    if verbs.findVerb(a) == "":
        return "Hey there partner, you made less sense then a goose chasing an aligator!"
    else:
        a = verbs.findVerb(a)
        a_out = verbs.ending(a)
        alt = random.choice(verbs.good_verbs)
        alt_out = verbs.ending(alt)
        if a in verbs.bad_verbs:
            return f"You are a god damn weirdo, man! {alt_out} is a muuuch safer alternative!"
        else:
            return f"Done diddly doo. {a_out} sound super duper nice!"



def sarah(a):
    for w in a.split():
        if verbs.findHello(w) and len(a.split()) < 3:
            return "Yeah, hey or whatever!"
    if verbs.findVerb(a) == "":
        return "Like can you actually talk english please. Jez-US!"
    else:
        a = verbs.findVerb(a)
        a_out = verbs.ending(a)
        sarah_verbs = ["cook", "read", "write", "relax", "kiss"]
        if a in sarah_verbs:
            return f"Yes! {a_out} sounds, like, suuuper nice to do! I like you or whatever"
        else:
            return f"I'm like not really into {a_out}. Can't you be more fun?"


def chris(a):
    for w in a.split():
        if verbs.findHello(w) and len(a.split()) < 3:
            return "Hi, do you want to feel my muscles?"
    if verbs.findVerb(a) == "":
        return "I don't understand you, bro. Maybe we should do some sport!"
    else:
        a = verbs.findVerb(a)
        a_out = verbs.ending(a)
        if a == 'play':
            l = [1, 2, 3, 4]
            r = random.choice(l)
            match r:
                case 1:
                    return f"Dude yes! I would really like to play some football! " \
                           f"Did you know I won a medal for best runner?"
                case 2:
                    return f"I would love to play, man! Jesus, I haven't played hockey in ages. You in?"
                case 3:
                    return f"Yees finally! You know, I'm somewhat of a boxer. Want to beat each other faces, man?"
                case 4:
                    return f"I can't wait! What do you want to play?"
        else:
            return f"Nah, man. I don't do {a_out}, dude. Let's leave it."