# How we can do this without enumerate function

names = ["inam" , "ikram" , "niamat"]
# pos = 0
# for name in names:
#     print(f"{pos} ----> {names}")
#     pos += 1

# with enumerate function

for pos, name in enumerate(names):
    print(f"{pos} ----> {names}")

def find_pos(l, target):
    for pos, name in enumerate(l):
        if name == target:
            return pos
        return -1
print(find_pos(names,'inam'))