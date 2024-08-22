import pyautogui
from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui as mouse
import math

gestureDict = {
    'Grab': [0, 0, 0, 0, 1],
    'Point': [0, 0, 0, 1, 1], 
    'Scroll': [1, 0, 0, 1, 0]
}

def Gesture(points):
    valueList = list(gestureDict.values())
    keyList = list(gestureDict.keys())
    
    if points in valueList:
        ind = valueList.index(points)   
        return keyList[ind]
    else: 
        return 'No Action'

# TODO
# Adjust the scaling to match properly
# Known issue that normalizing the coords is inaccurate
def Normalize_Coord(img, point):
    x, y, = point
    comH, comW = mouse.size()
    imgH, imgW = img.shape[:2]
    
    multiX = comH / imgH
    multiY = comW / imgW
    
    newX = math.floor(x * multiX)
    newY = math.floor(y * multiY)
    
    return newX, newY

def HandTrack():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            pHand = hands[0]
            # bbox = pHand["bbox"]
            centerPoint = pHand['center']
            fingers = detector.fingersUp(pHand)
            fingers.reverse()
            
            mouse.moveTo(Normalize_Coord(img, centerPoint))
            gest = Gesture(fingers)

            match gest:
                case 'Grab':
                    if pHand['type'] == "Right":
                        pyautogui.rightClick()
                    else:
                        pyautogui.leftClick()
                case 'Scroll':
                    scrollValue = 25 if img.shape[:2][0]/2 > centerPoint[1] else -25
                    pyautogui.scroll(scrollValue)
                case _:
                    pass

            # cv2.putText(img, gest, (bbox[0] + bbox[2] + 30, bbox[1] + bbox[3] + 30), cv2.FONT_HERSHEY_PLAIN,
            #                     2, (0, 255, 0), 2)
            
        # Display
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)
    
if __name__ == '__main__':
    HandTrack()