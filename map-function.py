# Map Function

numbers = [1,2,3,4]

def squares (a):
    return a**2
# print(map(square , numbers))
# square = list(map(square , numbers))
square = list (map(lambda a:a**2, numbers))
print(squares)

# list comp
square_new = [i**2 for i in numbers]
print(square_new)

new_list = []
for num in numbers:
    new_list.append(squares(num))
    print(new_list)

names = ["abc" , "abcd" , "abcde"]
length = map(len,names)
for i in length:
    print(i)
for j in length:
    print(j)