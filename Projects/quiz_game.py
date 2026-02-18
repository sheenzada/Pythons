print('Wlecome to my computer quiz')

playing = input('Do You Want to play?')

text = 'Tim IS GREAT!'
print(text.lower())

if playing.lower != 'yes':
    quit()
print("Okay! Let's Play :")
score = 0


answer = input("What does CPU stand for? ")

if answer == 'central processing unit':
    print('Correct!')
    score = score + 1
else:
    print('Incorrect!')

answer = input("What does GPU stand for? ")

if answer == 'graphics processing unit':
    print('Correct!')
    score += 1
else:
    print('Incorrect!')

answer = input("What does RAM stand for?")

if answer == 'random access memory':
    print('Correct!')
    score += 1
else:
    print('Incorrect!')

answer = input("What does PSU stand for?")

if answer == 'power supply':
    print('Correc t!')
    score += 1
else:
    print('Incorrect!')
print("You got " + str(score) + "questions correct!")
print("You got " + str((score / 4) * 100) + "%.")