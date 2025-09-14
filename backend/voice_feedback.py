
import pyttsx3

def give_audio_feedback(text_list):
    engine = pyttsx3.init()  # Move init inside function
    for line in text_list:
        engine.say(line)
    engine.runAndWait()
    engine.stop()
