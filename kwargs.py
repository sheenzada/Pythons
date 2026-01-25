# kwargs(keyword arguement)
#**kwargs (double star operator)
# kwargs as a parameter

def func(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}:{v}")
    # print(kwargs)
    # print(type(kwargs))
# Dictionary Unpacking
# func(first_name = "Inam" , last_name = "Ullah")

d = {'name' : 'Inam' , 'age' : 24}
func(**d)