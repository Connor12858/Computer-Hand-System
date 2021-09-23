import re
import time
import os
import cv2
import pyttsx3
import encryptionSystem as Es
import speech_recognition as sr
from pathlib import Path


key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
engine = pyttsx3.init()
r = sr.Recognizer()

adminPassword = "admin"


def voice():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        audio = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return audio


def speak(message):
    print(message)
    # engine.say(message)
    # engine.runAndWait()
    time.sleep(1)


def changeAdmin():
    speak("Please wait while we reset")
    folder_loc = os.getcwd() + "\\allowed_faces\\"
    photos = [os.path.join(folder_loc, f) for f in os.listdir(folder_loc) if
                 os.path.isfile(os.path.join(folder_loc, f))]

    for photo in photos:
        photoName = str(Path(photo).stem)
        if "_admin" in photoName:
            os.remove(photo)

    adminFile = open("data\\admin", "w")
    admin1 = Es.encrypt_message("Name:admin")
    admin2 = Es.encrypt_message("Nickname:admin")
    admin3 = Es.encrypt_message("Password:admin")
    admin4 = Es.encrypt_message("Gender:noun")
    admin5 = Es.encrypt_message("Age:100")
    admin6 = Es.encrypt_message("Birthday:2000/01/01")
    adminFile.write("{}\n{}\n{}\n{}\n{}\n{}".format(admin1, admin2, admin3, admin4, admin5, admin6))
    adminFile.close()

    createAdmin()


def createAdmin():
    speak("Setting up admin account")
    adminFile = open("data\\admin", "r+")
    adminContents = adminFile.readlines()
    adminLines = []
    for line in adminContents:
        adminLines.append(Es.decrypt_message(line))
    adminContents = "\n".join(adminLines)

    speak("What is the Admin Name?")
    name = voice()
    adminContents = re.sub("Name:[a-z]+", "Name:{}".format(name), adminContents)

    speak("What is the Admin Password?")
    password = voice()
    adminPassword = password
    adminContents = re.sub("Password:[a-z]{4,}", "Password:{}".format(password), adminContents)

    speak("What is the Admin Nickname?")
    nickname = voice()
    adminContents = re.sub("Nickname:[a-z]+", "Nickname:{}".format(nickname), adminContents)

    adminFile.seek(0)
    adminFile.write(Es.encrypt_message(adminContents))
    adminFile.truncate()

    adminFile = open("data\\admin", "r+")
    adminContents = adminFile.readlines()
    adminLines = []
    for line in adminContents:
        adminLines.append(Es.decrypt_message(line))
    adminContents = "\n".join(adminLines)
    print(adminContents)

    speak('Look at the camera for your picture')
    check, frame = webcam.read()
    cv2.imshow("Capturing", frame)
    time.sleep(5)
    cv2.imwrite(filename='allowed_faces\\{}_admin.jpg'.format(name), img=frame)
    speak("Captured")
    webcam.release()

    speak("Finalizing account details")
    userFile = open("data\\accounts", "a+")
    userContents = "\n\n{} [\n  Nickname:{}\n  Password:{}\n  Gender:noun\n  Age:100\n  Birthday:2000-01-01\n]".format(
                                                                                               name, nickname, password)
    userFile.seek(0)
    userFile.write(Es.encrypt_message(userContents))
    userFile.truncate()
    userFile.close()
    speak("Finished creating the admin account")


def createUser():

    speak("Setting up user's account")
    userFile = open("data\\accounts", "a+")

    speak("What is the User's Name?")
    name = voice()
    userContents = "\n\n{} [\n  Nickname:default\n  Gender:noun\n  Age:100\n  Birthday:2000-01-01\n]".format(name)
    print(userContents)

    speak("What is the User's Nickname?")
    nickname = voice()
    userContents = re.sub("Nickname:[a-z]+", "Nickname:{}".format(nickname), userContents)

    userFile.seek(0)
    userFile.write(Es.encrypt_message(userContents))
    userFile.truncate()
    userFile.close()

    userFile = open("data\\accounts", "r")
    userContents = userFile.readlines()
    userLines = []
    for line in userContents:
        userLines.append(Es.decrypt_message(line))
    userContents = "\n".join(userLines)
    print(userContents)
    userFile.close()

    speak('Look at the camera for your picture')
    check, frame = webcam.read()
    cv2.imshow("Capturing", frame)
    time.sleep(5)
    cv2.imwrite(filename='allowed_faces\\{}.jpg'.format(name), img=frame)
    speak("Captured")
    webcam.release()

    speak("Finished creating your account")
