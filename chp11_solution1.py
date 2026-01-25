# l = []

# if len (l) > 0:
#     print("not empty")
# else:
#     print("empty")

def two_power(num , *args):
    if args:
        return[i**num for i in args]
    else:
        return "You didn't pass any args"
nums = [1,2,3]
print(two_power(3,*[2,3]))