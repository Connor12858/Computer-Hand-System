import cv2
import face_recognition
import mediapipe as mp
import numpy as np
import pyautogui as mouse
import encryptionSystem as Es
import data_setup
import face_encodings as fe
import setup


def program(userName):
    # Should reply with name
    setup.speak("Hello {}".format(userName))

    # Declaring the MediaPipe solutions
    drawing_module = mp.solutions.drawing_utils
    hand_module = mp.solutions.hands

    # Get the computer screen size
    comWidth, comHeight = mouse.size()

    # Capturing video
    cap = cv2.VideoCapture(0)

    with hand_module.Hands(
            min_detection_confidence=0.8,
            max_num_hands=1,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, video = cap.read()
            if not success:
                print("Empty Frame")
                continue

            video = cv2.cvtColor(cv2.flip(video, 1), cv2.COLOR_BGR2RGB)
            video.flags.writeable = False
            display = hands.process(video)

            video.flags.writeable = True
            video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
            if display.multi_hand_landmarks:
                for hand_landmarks in display.multi_hand_landmarks:
                    drawing_module.draw_landmarks(
                        video, hand_landmarks, hand_module.HAND_CONNECTIONS)

                # Gets the thumb landmark for detecting left or right hand
                normalizedLandmarkThumb = hand_landmarks.landmark[4]

                # Get the landmarks needed for detecting hand positions
                normalizedLandmark20 = hand_landmarks.landmark[20]
                normalizedLandmark16 = hand_landmarks.landmark[16]
                normalizedLandmark12 = hand_landmarks.landmark[12]
                normalizedLandmark17 = hand_landmarks.landmark[17]
                normalizedLandmark13 = hand_landmarks.landmark[13]
                normalizedLandmark9 = hand_landmarks.landmark[9]
                normalizedLandmark8 = hand_landmarks.landmark[8]
                normalizedLandmark5 = hand_landmarks.landmark[5]

                # Preparing for mouse movement
                normalizedPalm = hand_landmarks.landmark[0]

                # Left hand controls
                if normalizedLandmarkThumb.x > normalizedLandmark17.x:

                    # MOVE MOUSE
                    mouseCords = drawing_module._normalized_to_pixel_coordinates(normalizedPalm.x,
                                                                                 normalizedPalm.y,
                                                                                 comWidth, comHeight)
                    mouse.moveTo(mouseCords)

                    # Left Click with left hand
                    if (normalizedLandmark12.y > normalizedLandmark9.y) & (
                            normalizedLandmark16.y > normalizedLandmark13.y) & (
                            normalizedLandmark20.y > normalizedLandmark17.y) & (
                            normalizedLandmark8.y > normalizedLandmark5.y):
                        mouse.leftClick()

                # Right Hand controls
                if normalizedLandmarkThumb.x < normalizedLandmark17.x:

                    mouseCords = drawing_module._normalized_to_pixel_coordinates(normalizedPalm.x,
                                                                                 normalizedPalm.y,
                                                                                 comWidth, comHeight)
                    mouse.moveTo(mouseCords)

                    # Right click with right hand
                    if (normalizedLandmark12.y > normalizedLandmark9.y) & (
                            normalizedLandmark16.y > normalizedLandmark13.y) & (
                            normalizedLandmark20.y > normalizedLandmark17.y) & (
                            normalizedLandmark8.y > normalizedLandmark5.y):
                        mouse.rightClick()

                # Scrolling with spider-man hands
                if (normalizedLandmark12.y > normalizedLandmark9.y) & (
                        normalizedLandmark16.y > normalizedLandmark13.y) & (
                        normalizedLandmark20.y < normalizedLandmark17.y) & (
                        normalizedLandmark8.y < normalizedLandmark5.y):

                    topDown = comHeight / 2

                    mouseX, mouseY = mouseCords
                    if mouseY > topDown:
                        mouse.scroll(-30)
                        continue
                    if mouseY < topDown:
                        mouse.scroll(30)
                        continue
                    continue

            # Create the video footage
            cv2.imshow('Hand Tracking', video)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyWindow('Hand Tracking')


def face_enter():
    video_capture = cv2.VideoCapture(0)

    known_face_encodings = fe.face_encode()
    known_face_names = fe.face_name()

    isAdmin = False
    isUser = False

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "No Match"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if "_admin" in name:
                        isAdmin = True
                    # break

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Face Recognition', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyWindow('Face Recognition')
    program(name)


if __name__ == "__main__":
    dataSetup = open("data\\dataSetUp", "r")
    dataString = dataSetup.read()
    dataContents = Es.decrypt_message(dataString)

    if dataContents == "False":
        print("Setting up data...")
        data_setup.fileCreation()
    dataSetup.close()

    accs = open("data\\accounts", "r")
    accsContent = Es.decrypt_message(accs.read())

    # if accsContent == "":
    # print("Creating Admin account...")
    # setup.createAdmin()
    # accs.close()

    face_enter()
