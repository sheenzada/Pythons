def func(name , *args, last_name = 'Unknown' , **kwargs):
    print(name)
    print(args)
    print(last_name)
    print(kwargs)

func('Inam',1,2,3 , a=1, b=2)
#     print(name)
#     print(age)
# func('Inam',18)