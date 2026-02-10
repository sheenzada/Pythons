
# import wikipedia

# topic = input ("Enter Keyword to search: ")
# print("="*30)
# print(f"Searching for: {topic}")
# print("="*30)

# res = wikipedia.summary(topic , sentences= 3)
# print(res)
# print("="*30)

import wikipedia

topic = input("Enter Keyword to search: ")

print("==============================")
print("Searching for:", topic)
print("==============================")

try:
    result = wikipedia.summary(topic, sentences=3)
    print(result)
except wikipedia.exceptions.DisambiguationError as e:
    print("Multiple results found. Try something more specific.")
except wikipedia.exceptions.PageError:
    print("No page found.")
