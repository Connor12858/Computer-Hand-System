import cv2
import mediapipe as mp
import numpy as np
import pyautogui as mouse


def program():
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


if __name__ == "__main__":
    program()
