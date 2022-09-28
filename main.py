import cv2
import mediapipe as mp
import pyautogui as mouse
import voice
import threading
from multiprocessing import Process


def program():
    # Declaring the MediaPipe solutions
    drawing_module = mp.solutions.drawing_utils
    hand_module = mp.solutions.hands

    # Get the computer screen size
    com_width, com_height = mouse.size()

    # Capturing video
    cap = cv2.VideoCapture(0)

    with hand_module.Hands(
            min_detection_confidence=0.8,
            max_num_hands=1,
            min_tracking_confidence=0.8) as hands:
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
                normalized_landmark_thumb = hand_landmarks.landmark[4]

                # Get the landmarks needed for detecting hand positions
                normalized_landmark20 = hand_landmarks.landmark[20]
                normalized_landmark16 = hand_landmarks.landmark[16]
                normalized_landmark12 = hand_landmarks.landmark[12]
                normalized_landmark17 = hand_landmarks.landmark[17]
                normalized_landmark13 = hand_landmarks.landmark[13]
                normalized_landmark9 = hand_landmarks.landmark[9]
                normalized_landmark8 = hand_landmarks.landmark[8]
                normalized_landmark5 = hand_landmarks.landmark[5]

                # Preparing for mouse movement
                normalized_palm = hand_landmarks.landmark[0]

                # Left hand controls
                if normalized_landmark_thumb.x > normalized_landmark17.x:

                    # MOVE MOUSE
                    mouse_cords = drawing_module._normalized_to_pixel_coordinates(normalized_palm.x,
                                                                                 normalized_palm.y,
                                                                                 com_width, com_height)
                    mouse.moveTo(mouse_cords)

                    # Left Click with left hand
                    if (normalized_landmark12.y > normalized_landmark9.y) & (
                            normalized_landmark16.y > normalized_landmark13.y) & (
                            normalized_landmark20.y > normalized_landmark17.y) & (
                            normalized_landmark8.y > normalized_landmark5.y):
                        mouse.leftClick()

                # Right Hand controls
                if normalized_landmark_thumb.x < normalized_landmark17.x:

                    mouse_cords = drawing_module._normalized_to_pixel_coordinates(normalized_palm.x,
                                                                                 normalized_palm.y,
                                                                                 com_width, com_height)
                    mouse.moveTo(mouse_cords)

                    # Right click with right hand
                    if (normalized_landmark12.y > normalized_landmark9.y) & (
                            normalized_landmark16.y > normalized_landmark13.y) & (
                            normalized_landmark20.y > normalized_landmark17.y) & (
                            normalized_landmark8.y > normalized_landmark5.y):
                        mouse.rightClick()

                # Scrolling with spider-man hands
                if (normalized_landmark12.y > normalized_landmark9.y) & (
                        normalized_landmark16.y > normalized_landmark13.y) & (
                        normalized_landmark20.y < normalized_landmark17.y) & (
                        normalized_landmark8.y < normalized_landmark5.y):

                    top_down = com_height / 2

                    mouse_x, mouse_y = mouse_cords
                    if mouse_y > top_down:
                        mouse.scroll(-70)
                        continue
                    if mouse_y < top_down:
                        mouse.scroll(70)
                        continue
                    continue

            # Create the video footage
            # cv2.imshow('Hand Tracking', video)
            # if cv2.waitKey(5) & 0xFF == ord('q'):
            #     break
    cap.release()
    # cv2.destroyWindow('Hand Tracking')


if __name__ == "__main__":
    program()

    # p = Process(target=voice.background_check(), args=())
    # p2 = Process(target=program(), args=())
    # p.start()
    # p.join()
    # p2.start()
    # p2.join()

    # t = threading.Thread(target=voice.background_check(), args=[])
    # t2 = threading.Thread(target=program(), args=[])
    # t.start()
    # t2.start()
