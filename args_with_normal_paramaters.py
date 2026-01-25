#  *args with normal paramater

def multiply_nums( num1,num2, *args):
    multiply = 1
    # print(num)
    print(args)
    for i in args:
        multiply *= i
    return multiply
print(multiply_nums(2,4,3,4))