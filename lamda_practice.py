# Lamda expression practice

# def is_even(a):
#     return a%2 == 0
# print (is_even(5))

# iseven2 = lambda a: a%2==0
# print(iseven2(6))

last_char = lambda s: s[-1]
print(last_char("Inam"))

def func(s):
    if len (s) >  5:
        return True
    return False
func = lambda s : True if len (s) > 5 else False
print(func("abcdefg"))