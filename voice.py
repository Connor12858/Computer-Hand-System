import pyttsx3

engine = None

def speak(text):
    global engine
    engine.say(text)
    engine.runAndWait()

def setup():
    global engine
    engine = pyttsx3.init()