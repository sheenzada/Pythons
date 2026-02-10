import random

print("="*30)
print("Guess The Number")
print("="*30)

while(True):
    computer = random.randint(1,10)
    user = int(input('Enter a number from 1 -10: '))
    print("="*30)

    if(user <1 or user>10):
        print("Enter number from 1 -10")
        print("-"*30)
    elif(user == computer):
        print("You Win !")
        break
    else:
        print("Try Again!")