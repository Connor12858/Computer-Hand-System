import cv2
import mediapipe as mp
import pyautogui as mouse
#import voice
import math
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
    # cv2.imshow('Hand Tracking', None)

    # Use Hand module
    with hand_module.Hands(
            min_detection_confidence=0.8,
            max_num_hands=1,
            min_tracking_confidence=0.8) as hands:
        
        # While video is capture do checks
        while cap.isOpened():
            success, video = cap.read()
            if not success:
                print("Empty Frame")
                continue
            
            # Get the video information needed
            video = cv2.cvtColor(cv2.flip(video, 1), cv2.COLOR_BGR2RGB)
            display = hands.process(video)

            # Detect hands
            video.flags.writeable = True
            video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
            if display.multi_hand_landmarks:
                # Draw the hands
                for hand_landmarks in display.multi_hand_landmarks:
                    drawing_module.draw_landmarks(
                        video, hand_landmarks, hand_module.HAND_CONNECTIONS)
                    
                # Create the video footage
                cv2.imshow('Hand Tracking', video)
                        
                # Move the mouse according to location
                mouse_cords = drawing_module._normalized_to_pixel_coordinates(hand_landmarks.landmark[8].x,
                                                                            hand_landmarks.landmark[8].y,
                                                                            com_width + 150, com_height + 150)
                if not mouse_cords == None:
                    mouse.moveTo(mouse_cords) #TODO make easier on left and top side
                
            # On 'q' quit and close everything
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyWindow('Hand Tracking')


# Entrypoint
if __name__ == "__main__":
    program()
