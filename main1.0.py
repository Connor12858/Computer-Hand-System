import cv2
import mediapipe as mp
import pyautogui as mouse
import math

def program():
    # Declaring the MediaPipe solutions
    drawing_module = mp.solutions.drawing_utils
    hand_module = mp.solutions.hands

    # Get the computer screen size
    com_width, com_height = mouse.size()

    # Capturing video
    cap = cv2.VideoCapture(0)

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
            results = hands.process(video)

            # Detect hands
            if results.multi_hand_landmarks:
                # Draw the hands
                for hand_landmarks in results.multi_hand_landmarks:
                    drawing_module.draw_landmarks(
                        video, hand_landmarks, hand_module.HAND_CONNECTIONS)
                    
                # Create the video footage
                cv2.imshow('Hand Tracking', video)
                
                # Move the mouse based on index point
                reg_coord = drawing_module._normalized_to_pixel_coordinates(hand_landmarks.landmark[8].x,
                                                                            hand_landmarks.landmark[8].y,
                                                                            com_width, com_height)
                        
                multi_coord = drawing_module._normalized_to_pixel_coordinates(1,1,com_width + 150,com_height + 150)
                
                if not reg_coord == None:
                    
                    # Check for which multiplier to apply
                    xMulti = 1
                    yMulti = 1
                    if reg_coord[0] > (com_width / 2):
                        xMulti = -1
                    if reg_coord[1] > (com_height / 2):
                        yMulti = -1
                    
                    top = math.floor(reg_coord[1] - (multi_coord[1] / 10))
                    bottom = com_height - math.floor(reg_coord[1] + (multi_coord[1] / 10))
                    right = com_width - math.floor(reg_coord[0] + (multi_coord[0] / 10))
                    left = math.floor(reg_coord[0] - (multi_coord[0] / 10))
                    print("Bottom:", bottom, "-", "Top", top, '-', 'left', left, '-', 'right', right)
                    
                    # Add the multi to the coords
                    mouseX = reg_coord[0] + (multi_coord[0] / 10) * xMulti
                    mouseY = reg_coord[1] + (multi_coord[1] / 10) * yMulti
                    mouse.moveTo(mouseX, mouseY)
                
            # On 'q' quit and close everything
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyWindow('Hand Tracking')


# Entrypoint
if __name__ == "__main__":
    program()
