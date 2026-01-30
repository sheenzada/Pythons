

class Name(ValueError):
    pass


def validate(name ):
    if len (name) < 8:
        raise Name('name is too short ')
    
username = input ('Enter your Name :')
validate(username)
print(f'Hello {username}')

