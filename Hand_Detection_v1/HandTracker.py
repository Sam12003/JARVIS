import math
import cv2
import time
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands.Hands()

wCam, hCam = 640, 480

FingerUp = [1,1,1,1,1] # Which Finger Is Up [Thumb, Index Finger, Middle Finger, Ring Finger, Pinky Finger]

# Has Perfored a task
HasClicked = False
IsZooming = False
ZoomStartPoint = 350

Video_Capture = cv2.VideoCapture(0)
Video_Capture.set(3,wCam)
Video_Capture.set(4,hCam)

def DrawPoint():

    text = ""
    cv2.putText(frame, text, (100, 200), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0),1)

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

    global HasClicked, FingerUp, IsZooming, ZoomStartPoint

    # Zoom Feature
    if FingerUp == [1,1,1,0,0] or IsZooming == True: # if the thumb, index finger and middle finger are up or zomming is in process

        if GetDistance(8, 12) <= 45 : # Zoom IN

            if  GetDistance(4,12) <= 45: # Start Of Zoom

                IsZooming = True
                ZoomStartPoint = GetDistance(4,12) # Asign The Start Point Of Zooming
                print("Zoom In Start")

            if GetDistance(4,12) >= 150 and IsZooming == True: # End Of Zoom
                IsZooming = False
                print("Stop Zoom")

            elif GetDistance(4,12) > ZoomStartPoint and IsZooming == True: # Zooming in
                pyautogui.keyDown('ctrl')
                pyautogui.press('=')
                pyautogui.keyUp('ctrl')
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
                pyautogui.keyDown('ctrl')
                pyautogui.press('-')
                pyautogui.keyUp('ctrl')
                print("Zomming out")
    
    # Click when index and thumb touch
    if GetDistance(4,8) <= 35 and GetDistance(8,12) >= 45:
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
