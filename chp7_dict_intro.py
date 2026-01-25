# dictionaries intro
# Q - why we use dictionaries?
# A - because a limitations of list , list are not enough to represent
# real data .

# Example
user = ['Inamullah' , 24 , ['coco' , 'kimi no na wa'],['awakening' , 'fairy tale']]
# this list contains user name , age , fav movie , fav tunes
# you can do this but this is not a good way to do this

# Q - what are dictionaries
# A - unordered collections of data in key : value pair.

# How to create dictionaries
user = {'name' : 'Inamullah' , 'age' : 24}
# print(user)
# print(type(user))

# Second method to create dictionary
user1 = dict ( name = 'Inamullah' , age = 24 )
# print(user1)

# how to access data from to dictionary
# NOTE - There is no indexing because of unordered collections of data.
# print (user['name'])
# print(user['age'])

# which type of data a dictionary can store ?
# anything
# numbers , string , list , dictionary

user_info = {
    'name': 'Inamullah',
    'age' : '24',
    'fav_movies' : ['coco' , 'kimi no na wa'],
    'fav_tunes' : ['awakening' , 'fairy tale'],
}
# print(user_info["fav_movies"])

# how to add data to empty dictionary
user_info2={}
user_info2=['name'],'ikramullah'
user_info2=['age'],'10'

print(user_info2)
