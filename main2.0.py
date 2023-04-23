from cvzone.HandTrackingModule import HandDetector
import cv2
import voice
import face_recognition
import pyautogui as mouse
import math

gestureDict = {
    'Grab': [0, 0, 0, 0, 0],
    'Point': [0, 0, 0, 1, 0], 
    'Rock': [1, 0, 0, 1, 1],
    'Shrink': [0, 0, 0, 1, 1],
    'Grow': [1, 0, 0, 0, 1]
}

def Gesture(points):
    valueList = list(gestureDict.values())
    keyList = list(gestureDict.keys())
    
    if points in valueList:
        ind = valueList.index(points)
        return keyList[ind]
    else: 
        return 'No Action'

def Normalize_Coord(img, point):
    x, y = point
    comH, comW = mouse.size()
    imgH, imgW = img.shape[:2]
    
    multiX = comH / imgH
    multiY = comW / imgW
    
    newX = math.floor(x * multiX)
    newY = math.floor(y * multiY)
    
    return newX, newY

def GetPerson():
    pass

def HandTrack():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)

        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]  # List of 21 Landmark points
            bbox = hand1["bbox"]  # Bounding box info x,y,w,h
            centerPoint = hand1['center']  # center of the hand cx,cy
            handType = hand1["type"]  # Handtype Left or Right
            fingers = detector.fingersUp(hand1)
            fingers.reverse()
            
            mouse.moveTo(Normalize_Coord(img, centerPoint))
            gest = Gesture(fingers)
            print(bbox)
            cv2.putText(img, gest, (bbox[0] + bbox[2] + 30, bbox[1] + bbox[3] + 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (0, 255, 0), 2)
            
        # Display
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
if __name__ == '__main__':
    voice.setup()
    name = GetPerson()
    voice.speak('Hello', name)
    HandTrack()