import random
import verbs

bots = ["bobby", "billy", "sarah", "chris"]

def billy(a):
    a_out = verbs.ending(a)
    alt = random.choice(verbs.verbs)
    alt_out = verbs.ending(alt)
    return f"{a_out} sounds super duper cool, boy! Maybe even {alt_out} would work!", alt


def bobby(a):
    a_out = verbs.ending(a)
    if a in verbs.bad_verbs:
        return f"Billy you are a god damn weirdo, man! {a_out} is a muuuch safer alternative!"
    else:
        return f"Done diddly doo. {a_out} sound super duper nice!"

def sarah(a):
    a_out = verbs.ending(a)
    sarah_verbs = ["cook", "read", "write", "relax", "kiss"]
    if a in sarah_verbs:
        return f"Yes! {a_out} sounds, like, suuuper nice to do! I like you or whatever"
    else:
        return f"I'm like not really into {a_out}. Can't you be more fun?"

def chris(a):
    a_out = verbs.ending(a)
    if a == 'play':
        l = [1,2,3,4]
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