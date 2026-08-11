from random import randint

numseek = 7
temp = 0
Rnum = []
for i in range (10):
    Rnum.append(randint(1,99))
    print(Rnum)

for i in range (len(Rnum)):
    if(numseek == Rnum[i]):
        temp = temp + 1
    if temp > 0:
        print("7 is on index: " . Rnum.index(7))
    else:
        print('7 is not in the list')