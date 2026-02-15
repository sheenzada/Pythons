

responses = {
    'hi' : 'Hey! there',
    'hello': 'Hello! Hoe can i help you',
    'how are you' : 'I am just a chartbot but i am good',
    'bye' : 'Goodbye! Nice to meet you'
}

def chart_boot():
    while True:
        user_input = input("You :").lower()
        if user_input == 'exit':
            print('Goodbye!')
            break
        response = responses.get(user_input , 'Sorry i donot');
        print(f'Chartbot :{response}')

chart_boot()