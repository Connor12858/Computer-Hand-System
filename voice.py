import speech_recognition as sr
import pyttsx3
import pyautogui as mouse

keywords = ["Connor", "Conner"]
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)


def text_input():
    engine.say("Typing")
    engine.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                if text == "enter":
                    background_check()
                    return
                mouse.typewrite(text)
            except sr.UnknownValueError:
                print("Could not understand")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


def main_check():
    engine.say("Hello There")
    engine.runAndWait()
    background_check()


def background_check():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                usr_input = r.recognize_google(audio)
                for keyword in keywords:
                    if usr_input == keyword:
                        main_check()
                        return
                    if usr_input == "input text" or usr_input == "enter text":
                        text_input()
                        return
            except sr.UnknownValueError:
                print("Could not understand")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


if __name__ == "__main__":
    background_check()
