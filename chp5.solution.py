# define a function which will take list as a argument and this function

# def square_list(l):
#     square = []
#     for i in l:
#         square.append(i**2)
#     return square
# # list , str
# numbers = list(range(1,11))
# print(square_list(numbers))
#-------------------------------------------------------------------------------#
## will return a reversed list
2
# Examples
# [1 , 2 , 3 , 4] ---> [4 , 3 , 2 , 1]
# ['word1' , 'word2'] ---> ['word2' , 'word1']

# Note you simply do this with reverse method or [::-1]

# but try to do this with the help of append and pop method

# def reverse_list(l):
#     return l[::-1]

# def reverse_list(l):
#     r_list = []
#     for i in range(len(l)):
#         popped_item = l.pop()
#         r_list.append(popped_item)
#     return r_list
# numbers = [1 , 2 , 3 , 4]
# print(reverse_list(numbers))

#  -------------------------------------------------------------#
# return list with reverse of every element in that list 
# example
# ['abc' , 'tuv' , 'xyz'] ---> ['cba' , 'vut' , 'zyx']

def reverse_elements(l):
    elements = []
    for i in l:
        elements.append(i[::-1])
    return elements
words = ['abc' , 'tuv' , 'xyz']
print(reverse_elements(words))