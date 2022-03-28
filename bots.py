import random
import verbs

bots = ["alice", "bob", "dora", "chuck", "bobby", "billy"]


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


def chuck(a, b):
    if b in verbs.bad_verbs:
        return "YES! Time for some {}!!".format(b)
    elif b in verbs.good_verbs:
        return "{} is so boooriiiing! I'm not doing that".format(b)
    return "I don't care!"


# -------------------------------------------------------------


def billy(a, b=None):
    alt = random.choice(verbs.verbs)
    return f"{a + 'ing'} sounds super duper cool, boy! Maybe even {alt + 'ing'} would work!", alt


def bobby(a, b=None):
    if a in verbs.bad_verbs:
        return f"Billy you are a god damn weirdo, man! {a + 'ing'} is a muuuch safer alternative!"
    else:
        return f"Done diddly doo billy. That sound super duper nice!"
