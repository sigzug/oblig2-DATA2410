
### OKAY svar

# Finding words that need different ending
def ending(word):
    if 'e' in word[-1] or 'y' in word[-1]:
        word = word[:-1]
        return word + 'ing'
    else:
        return word + 'ing'

bad_verbs = ["accuse", "beat", "bite", "break", "kill", "crunch", "burn", "creep", "cry", "cut",
             "disagree", "fail", "fight", "hit",  "lie", "swear", "tear", "weep"]

good_verbs = ["achieve", "ask", "arrange", "bathe", "bake", "build", "carry", "cook", "dance", "sing",
              "discuss", "drink", "drive", "eat", "explain", "forget", "hide", "hug", "kiss", "laugh", "love",
              "read", "relax", "shake", "speak", "talk", "think", "watch", "win", "write", "play"]

verbs = bad_verbs + good_verbs