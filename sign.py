import os

details = []

print("_"*30)
print("Signup Here")
print("_"*30)

name = input("Enter Name :")
password = input("Enter Password :")
details.append(name)
details.append(password)
os.system('cls')

print("_"*30)
print("Login Now")
print("_"*30)

while(True):
    name=input("Enter name :")
    password = input("Enter Password :")
    if (name == details[0] and password == details[1]):
        print("Login Success!")
        break
    else:
        print("Wrong Username or Password Please try again")
        print("_"*30)