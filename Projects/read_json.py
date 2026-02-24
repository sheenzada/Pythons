import json

with open('data.json', 'r') as f:
    data = json.load(f)
    print("name: ", data['name'])
    print("age: ", data['age'])
    print("id: ", data['id'])