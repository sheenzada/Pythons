import pyttsx3

engine = pyttsx3.init()

# --- Optional Customization ---
# Set the speed (default is usually 200)
engine.setProperty('rate', 175) 

# Set volume (0.0 to 1.0)
engine.setProperty('volume', 0.9)

# Get available voices and switch to a different one (usually index 1 is female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
# ------------------------------

text = input("Enter the text you want to convert to audio: ")

if text.strip():
    print("Converting...")
    engine.save_to_file(text, 'output_audio.wav')
    engine.runAndWait()
    print("Done! File saved as 'output_audio.wav'")
else:
    print("You didn't enter any text!")