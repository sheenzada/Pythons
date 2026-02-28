import speech_recognition as sr
import time

def start_voice_tracking():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Adjust for ambient noise (background hum)
    # This helps the "tracking" be more accurate
    with sr.Microphone() as source:
        print("--- Calibrating for background noise... ---")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        recognizer.energy_threshold = 300  # Sensitivity level
        print("--- Tracking Active. Speak into the mic! ---")

    def callback(recognizer, audio):
        """
        This function is called every time a voice segment is 'tracked'
        """
        try:
            print("🔍 Voice detected, processing...")
            # Use Google's free web API for transcription
            text = recognizer.recognize_google(audio)
            print(f"🗣️  You said: {text}")
        except sr.UnknownValueError:
            print("❓ Voice tracked, but couldn't understand the words.")
        except sr.RequestError as e:
            print(f"❌ Connection error: {e}")

    # Start the background 'tracking' thread
    # phrase_time_limit keeps the segments short for faster response
    stop_listening = recognizer.listen_in_background(sr.Microphone(), callback, phrase_time_limit=5)

    try:
        while True:
            time.sleep(0.1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\n--- Stopping Voice Tracker ---")
        stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    start_voice_tracking()