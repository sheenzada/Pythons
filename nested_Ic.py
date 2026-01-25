# list comprehension in nested list

example = [[1,2,3] , [1,2,3] , [1,2,3]]
neste_comp = [[i for i in range (1,4)] for i in range(3) ]
print(neste_comp)

new_list =[]
for j in range(3):
    new_list.append([1,2,3])