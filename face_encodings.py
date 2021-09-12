import face_recognition
import os
from pathlib import Path

folder_loc = os.getcwd() + "\\allowed_faces\\"


def face_encode():
    known_face_encodings = []

    onlyFiles = [os.path.join(folder_loc, f) for f in os.listdir(folder_loc) if
                 os.path.isfile(os.path.join(folder_loc, f))]
    print("Got Files")

    fileNum = 1
    for i in os.listdir(folder_loc):
        image = folder_loc + i
        print(image)
        image = face_recognition.load_image_file(image)
        print("1")
        image_encoding = face_recognition.face_encodings(image)
        print("2")
        known_face_encodings.append(image_encoding[0])
        print("Encoded {}/{}".format(fileNum, len(onlyFiles)))
        fileNum = fileNum + 1

    return known_face_encodings


def face_name():
    known_face_names = []

    onlyFiles = [os.path.join(folder_loc, f) for f in os.listdir(folder_loc) if
                 os.path.isfile(os.path.join(folder_loc, f))]
    print("Got Names")

    nameNum = 1
    for file in onlyFiles:
        known_face_names.append(str(Path(file).stem))
        print("Name {}/{}".format(nameNum, len(onlyFiles)))
        nameNum += 1

    return known_face_names
