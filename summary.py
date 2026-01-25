#strings
name="InamUllah"
#name[2]= "1"
print(name.replace("a","A",1))
print(name)
#string indexing
print(name[-1])
#string slicing
print(name[0:1:5])
#take user input
age=int(input("enter your age :"))
print(age)
#take two users input
user_name, age=input("enter your name and age :").split()
print(user_name)
print(age)
#len function
print(len(name))
#lower,upper,title method
print(name.title())
#find,replace,center method
r_pos = name.find("l")
r_pos_2= name.find("l",r_pos + 1)
print(r_pos_2)
#strings are immutable