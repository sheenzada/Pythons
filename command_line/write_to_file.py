
# 'w' , "a" , 'r+'




# "r"
# with open ('file.txt' , 'r') as  f:
#     data = f.read()
#     print(data)


# W ....
# with open ('file.txt' ,'w') as f:
#     f.write('please do it')


# "r+"
# with open('file.txt' , "r+") as f:
#     f.write('please do it')

with open ('file.txt' ,'r+') as f:
    f.seek(len(f.read()))
    f.write('Please Do It')