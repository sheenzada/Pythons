# looping in tuples
# tupel with one element
# tuple without parenthesis
# tuple unpacking
# list inside tuple 
# some functions that you can use with tuples

mixed = (1,2,3,4.0)

# for loop and tuple
# for i in mixed:
#     print(i)
# Note - you can use while loop too


# tuples with one element
nums = (1,)
words=('word1',)
# print(type(nums))
# print(type('words'))

# tuples without parenthesis
guitars = 'yamaha' , 'baton rouge' , 'taylor'
# print(type(guitars))

# tuple unpacking
guitarists = ('Maneli jamal' , 'Eddie Van Deer Meer' , 'Andrew Foy')
guitarist1 , guitarist2 , guitarist3 = (guitarists)
# print(guitarist2)

# list inside tuples
favorites = ('southern magnolia',['Tokyo Ghoul Theme','landscape'])
favorites[1].pop()
favorites[1].append("we made it ")
# print(favorites)

# min() , max , sum
print(sum(mixed))