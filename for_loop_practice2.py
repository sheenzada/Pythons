# practice for loop
# ask user name and count each character
# "Inam Ullah"
# I : 1
# n : 1
# a : 2
# m : 4
#   : 1
# U : 1

name=input("Enter your name : ")
temp=""
for i in range (len(name)):
    if name [i] not in temp:
        print(f"{name[i]}: {name.count(name[i])}")
        temp += name[i]