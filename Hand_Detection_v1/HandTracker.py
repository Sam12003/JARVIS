import math
import cv2
import time
import mediapipe as mp
import pyautogui
import pydirectinput
import sys

sys.path.append('F:\python\JARVIS')
from Commands import *

mp_hands = mp.solutions.hands.Hands()

wCam, hCam = 640, 480
width, height= pyautogui.size()

FingerUp = [1,1,1,1,1] # Which Finger Is Up [Thumb, Index Finger, Middle Finger, Ring Finger, Pinky Finger]
FingerStartPoint = [(0,0),(0,0),(0,0),(0,0),(0,0)] #Finger position (x,y) [Thumb, Index Finger, Middle Finger, Ring Finger, Pinky Finger]
AllFingerWereUp = False
IndexAndMiddleWereUp = False
ActivatePanMouse = False
ActivateMoveMouse = False

MouseMoveSensitivity = 0.5

msg = ""

# Has Perfored a task
HasClicked = False
IsZooming = False
ZoomStartPoint = 350

Video_Capture = cv2.VideoCapture(0)
Video_Capture.set(3,wCam)
Video_Capture.set(4,hCam)

def DrawPoint():

    global msg
    cv2.putText(frame, msg, (100, 200), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0),1)

    for i in range(0,20):
                x1 = hand_landmarks.landmark[i].x * wCam
                y1 = hand_landmarks.landmark[i].y * hCam

                center = (int(x1), int(y1)) 

                if i < 20 and i != 4 and i != 8 and i != 12 and i != 16:
                        
                    x2 = hand_landmarks.landmark[i+1].x * wCam
                    y2 = hand_landmarks.landmark[i+1].y * hCam

                    center2 = (int(x2), int(y2)) 

                    if i == 0 or i == 5 or i == 9 or i == 13 or i == 17:

                        cv2.line(frame,center,center2,(0,252,0))
                        
                        j = i - 4

                        if j < 0:
                           j = 17

                        x2 = hand_landmarks.landmark[j].x * wCam
                        y2 = hand_landmarks.landmark[j].y * hCam
                    
                    center2 = (int(x2), int(y2)) 

                    cv2.line(frame,center,center2,(0,252,0))
 

                cv2.circle(frame, center, 2, (0,0,255), 2)

def DetectFinger():
    global FingerUp
    FingerUp = [1,1,1,1,1]
    
    if(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x): # Thumb Down
        FingerUp[0] = 0

    if(hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y): # Index Finger Down
        FingerUp[1] = 0

    if(hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y): # Middle Finger Down
        FingerUp[2] = 0

    if(hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y): # Ring Finger Down 
        FingerUp[3] = 0
        
    if(hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y): # Pinky Finger Down
        FingerUp[4] = 0

def GetDistance(Landmark1ID, Landmark2Id):
    x1 = int(hand_landmarks.landmark[Landmark1ID].x * wCam)
    x2 = int(hand_landmarks.landmark[Landmark2Id].x * wCam)
    y1 = int(hand_landmarks.landmark[Landmark1ID].y * hCam)
    y2 = int(hand_landmarks.landmark[Landmark2Id].y * hCam)

    point1 = (x1,y1)
    point2 = (x2,y2)

    distance = math.dist(point1,point2)
    
    return distance

def DetectCommand():

    # Detect the command to be proceesed based on finger movement

    global HasClicked, FingerUp, IsZooming, ZoomStartPoint, msg, ActivateMoveMouse, ActivatePanMouse, AllFingerWereUp, FingerStartPoint, IndexAndMiddleWereUp

    # Zoom Feature
    if FingerUp == [1,1,1,0,0] or IsZooming == True and FingerUp[3] != 1 and FingerUp[4] != 1: # if the thumb, index finger and middle finger are up or zomming is in process

        if GetDistance(8, 12) <= 45 : # Zoom IN

            if  GetDistance(4,12) <= 45: # Start Of Zoom

                IsZooming = True
                ZoomStartPoint = GetDistance(4,12) # Asign The Start Point Of Zooming
                print("Zoom In Start")

            if GetDistance(4,12) >= 150 and IsZooming == True: # End Of Zoom
                IsZooming = False
                print("Stop Zoom")

            elif GetDistance(4,12) > ZoomStartPoint and IsZooming == True: # Zooming in
                ZoomIn()
                print("Zomming in")

        else: # Zoom Out
            
            if GetDistance(4,12) >= 150: # Start Of Zoom

                IsZooming = True
                ZoomStartPoint = GetDistance(4,12) # Asign The Start Point Of Zooming
                print("Zoom Out Start")

            if GetDistance(4,12) <= 45 and IsZooming == True: # End Of Zoom
                IsZooming = False
                print("Stop Zoom")

            elif GetDistance(4,12) < ZoomStartPoint and IsZooming == True: # Zooming in
                ZoomOut()
                print("Zomming out")
    
    # Move Mouse
    if FingerUp == [0,1,1,0,0]:
        FingerStartPoint[0] = (reMap(hand_landmarks.landmark[0].x,.95,0.1,width,0),reMap(hand_landmarks.landmark[0].y,.95,0.1,height,0))
        IndexAndMiddleWereUp = True
        ActivateMoveMouse = False

    if FingerUp == [0,0,0,0,0] and IndexAndMiddleWereUp == True:
        IndexAndMiddleWereUp = False
        ActivateMoveMouse = True

    if ActivateMoveMouse == True:
        try:
            pyautogui.move(reMap(hand_landmarks.landmark[0].x,.95,0.1,width,0) - FingerStartPoint[0][0], reMap(hand_landmarks.landmark[0].y,.95,0.1,height,0) - FingerStartPoint[0][1]) # Relative to origin position
        except Exception as e:
            pass

        FingerStartPoint[0] = (reMap(hand_landmarks.landmark[0].x,.95,0.1,width,0),reMap(hand_landmarks.landmark[0].y,.95,0.1,height,0))

    # Pan Around (Panning)
    if FingerUp == [1,1,1,1,1]:

        # Disable Mouse Movement
        ActivateMoveMouse = False

        # check if al finger are up
        FingerStartPoint[0] = (reMap(hand_landmarks.landmark[0].x,.95,0.1,width,0),reMap(hand_landmarks.landmark[0].y,.95,0.1,height,0))

        # Stop Storcut of panning
        pydirectinput.keyUp('shift') # for blender
        pydirectinput.mouseUp(button='middle')

        ActivatePanMouse = False # Deactivate Mouse Moving Feature
        AllFingerWereUp = True # Activate All Finger Are Up to let the next if statement know that all fingers were up

    if IndexAndMiddleWereUp == True:
        AllFingerWereUp = False

    if FingerUp == [1,0,0,0,0] and AllFingerWereUp == True: # check if all fingers were up and then check if after that the figers were closed
        print("hi")
        AllFingerWereUp = False # Deactivate all fingers were up 
        ActivatePanMouse = True # Activate Move Mouse Feature

        # add movement (panning)

        if("Blender" in gw.getActiveWindow().title):
            pydirectinput.keyDown('shift') # for blender

        pydirectinput.mouseDown(button='middle')
    
    if ActivatePanMouse == True:
        try:
            # Move Mouse
            pyautogui.move(reMap(hand_landmarks.landmark[0].x,.95,0.1,width,0) - FingerStartPoint[0][0], reMap(hand_landmarks.landmark[0].y,.95,0.1,height,0) - FingerStartPoint[0][1]) # Relative to origin position
        except Exception as e:
            pass
        
        FingerStartPoint[0] = (reMap(hand_landmarks.landmark[0].x,.95,0.1,width,0),reMap(hand_landmarks.landmark[0].y,.95,0.1,height,0))

    # Click when index and thumb touch
    if GetDistance(4,8) <= 35 and GetDistance(8,12) >= 45 and FingerUp != [0,0,0,0,0]:
        if HasClicked == False:
            # pyautogui.click()
            print("click")
            print(FingerUp)
            HasClicked = True
    else:
        HasClicked = False

while True:
    ret, frame = Video_Capture.read()

    frame = cv2.flip(frame,1)

    results = mp_hands.process(frame)

    if results.multi_hand_landmarks:
        # Hands were detected

        for hand_landmarks in results.multi_hand_landmarks:
            # Do something with the detected hand
            DrawPoint()
            DetectFinger()
            DetectCommand()
            ...

    else:
        # No hands were detected
        ...

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) == ord('q'):
       Video_Capture.release()
       cv2.destroyAllWindows()
