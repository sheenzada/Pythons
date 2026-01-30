# open function


## ..................readfile ............

# f = open('file 1.txt')
# print(f.read())
# f.close()

## ...............read method ...............

# f = open('file 1.txt')
# print(f.read())
# print(f.read())

# f.close()


## ...........tell method ..............

# f= open('file 1.txt')
# print(f'cursor position -{f.tell()}')
# print(f.read())
# print(f'cursor position -{f.tell()}')
# print(f.read)
# f.close()


## .......... seek method ..........

# f = open('file 1.txt')
# print(f'cursor position - {f.tell()}')
# print(f.read())
# print(f'cursor position - {f.tell()}')
# print('before seek method')
# f.seek(0)
# print('after seek method')
# print(f'cursor position - {f.tell()}')
# print(f.read())
# f.close()


## ........... readline method ............

# f = open('file 1.txt')
# print(f.readline() , end='')
# print(f.readline())
# print(f.readline())
# f.close()


## .......... readlines method .................

# f = open('file 1.txt')
# lines = f.readlines()
# for line in lines:
#     print(line, end='')
# f.close()


## .............. close method ..............
f= open(r"E:\new_folder\file1.txt")
print(f.closed)
# print(f.name)
f.close()

print(f.closed)
