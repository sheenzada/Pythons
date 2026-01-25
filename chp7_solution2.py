# users = {
#     'name' : 'Inamullah',
#     'age' : 18,
#     'fav_movies' : ['coco' , 'avengers'],
#     'fav_songs' : ['song1' , 'song2']
# }
user = {}

name = input('What is your name : ')
age = input('What is your age :' )
fav_movies = input('your fav movies seperated by comma , ').split(',')
fav_songs = input('your fav songs seperated by comma , ').split(",")
user['name']=name
user['age']=age
user['fav_movies']=fav_movies
user['fav_songs']=fav_songs
# print(user)
for key, value in user.items():
    print(f'{key} : {value}')