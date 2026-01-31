
# f= open('file 1.txt')
# f.read()
# f.close()
    
# with block
# context manager

with open ('file 1.txt') as f:
    data = f.read()
    print(data)
print(f.closed)