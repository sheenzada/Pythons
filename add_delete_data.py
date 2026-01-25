# add and delete data
user_info = {
    'name' : 'Inamullah',
    'age' : 24,
    'fav_movies' : ['coco' , 'kimi no na wa'],
    'fav_tunes' : ['awakening' , 'fairy tale'],

}

# # How to add data
# user_info['fav_songs'] = ['song1' , 'song2']
# print(user_info)

# pop method
# popped_item = user_info.pop('fav_tunes')
# print(f'popped item is {popped_item}')
# print(user_info)

# pop method
popped_item = user_info.pop('age')
print(type(popped_item))
print(user_info)

# popitem method 
# popped_item = user_info.popitem()
# print(user_info)
# print(type(popped_item))