verbs = ["sing"]
# verbs  = ["sing","dance","carol"] ect
#badverbs  = [" "," ","  "]  you should think about it
#Hi works = ["hi","hej","hello",Hei] 
message = "Why don't we call?"

for v in verbs:
    if v in message:
        print("Yes")
    else:
        print("No")
