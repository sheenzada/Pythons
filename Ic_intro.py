# list comprehension
# with the help of list comprehension we can create of list in one line 

# create a list of squares from 1 to 10

# squares = []
# for i in range(1 , 11):
#     squares.append(i**2)
# print(squares)

# square2 = [ i**2 for i in range(1,11)]
# print(square2)

# negative = []
# for i in range(1,11):
#     negative.append(-i)
# print(negative)

# new_negative = [ -1 for i in range ( 1 , 11)]

names = [ 'Inamullah' , 'Ikramullah' , 'Niamatullah']
# new_list = ['I' , 'I' , 'N']
# new_list = []
# for name in names:
#     new_list.append(name[0])
# print(new_list)

new_list2 = [names[0] for names in names]
print(new_list2)