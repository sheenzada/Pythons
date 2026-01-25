# if elif else statement

# show ticket pricing 
# 1 to 3(Free)
# 4 to 10(150)
# 11 to 60(260)
# above 60 (200)

age=input("Please input your age :")
age=int(age)

if age==0 or age < 0:
    print("You can't watch")
elif 0<age<3:
    print("Ticket Price : Free")
elif 3<age<10:
    print("Ticket Price : 150")
elif 11<age<60:
    print("Ticket Price : 260")
else:
    print("Ticket Price : 200")
