name= input("Please inter your name :")
# Inamullah Khan 

# Inam , len -1 = 3
# name.count("I") , name.count(name[0]) = 1
# name.count("n") , name.count(name[1]) = 1
# name.count("a") , name.count(name[2]) = 1
# name.count("m") , name.count(name[3]) = 1

# output
# name[0] = h : 2
# I : 1
# n : 1
# a : 1
# m : 1

i = 1

while i < len(name):
    print(f"{name[i]} : {name.count(name[i] )}")
    i += 1

