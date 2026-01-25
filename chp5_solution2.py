# def filter_odd_even(l):
#     odd_nums = []
#     even_nums = []
#     for i in l:
#         if i % 2 == 0:
#             even_nums.append(i)
#         else:
#             odd_nums.append(i)
#     output = [odd_nums , even_nums]
#     return output
# nums = [1,2,3,4,5,6,7]
# print(filter_odd_even(nums))
##------------------------------------------------------------##
# logic
def common_finder(l1 , l2):
    output=[]
    for i in l1:
        if i in l2:
            output.append(i)
    return output
print(common_finder([1,2,5,8] , [1,2,7,6]))