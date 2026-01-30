

# print(f.rea.txtdline())
# print(f.readline())
# print(f.readline())
# print(f'cursor position - {f.tell()}')
# print(f.read())
# print(f'cursor position - {f.tell()}')
# print(f'befor seek method ')
# f.seek(0)
# print('after seek method ')
# print(f'cursor position - {f.tell()}')
# print(f.read())


f = open('file1.txt')
# lines = f.readlines()
# print(len(lines))

# for line in lines :
#     print(line)
# print(f.closed)

for line in f.readlines()[:2]:
    print(line , end= '')

f.close()

# print(f.closed)
