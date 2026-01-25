# fromkeys
# d1 = { 'name' : 'unknown' , 'age' : 'unknown' }
# d=dict.fromkeys(('name' , 'age' , 'height') , 'unknown')
# d = dict.fromkeys(("abc"),'unknown')
# d = dict.fromkeys(range(1,11),'unknown')
# d = dict.fromkeys( [ 'name' , 'age' ] , ['unknown' , 'unknown'] )
# print(d)

# get method (useful)
d = { 'name' : 'InamuUllah' , 'age' : 'unknown' }
# d = {}

# print(d['name'])
# print(d.get('names')) better

# if name in d:
#     print('present')
# else:
#     print('not present')

# if d.get('names'):
#     print('present')
# else:
#     print('not present')
# if None ----->  False , else -----> True

# d.clear
# print(d)

# d1 = d.copy()
d1 = d
# print(d1.popitem())
# print(d1 is d)
# print(d1==d)
print(d1 is d)
