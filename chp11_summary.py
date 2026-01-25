def add(a,b):
    return a + b
def new_add(*args):
    # 1,2,3,4
    # (1,2,3,4)
    total = 0
    for num in args:
        total += num
    return total
# print(new_add(1,2,3))
l = [1,2,3]
print(new_add(*l))