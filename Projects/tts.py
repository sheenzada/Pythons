
# # pip install pyttsx3

# import pyttx3
# engine = pyttx3.init()

# text = input ('Enter Your Text')

# engine.save_to_file(
#     text = text, filename='audio.mp3'

# )
# engine.runAndWait()
# print("Andio Saved Successfully!")


# pip install pyttsx3

import pyttsx3

engine = pyttsx3.init()

text = input("Enter your text: ")

engine.save_to_file(text, 'audio.mp3')
engine.runAndWait()

print("Audio saved successfully!")
