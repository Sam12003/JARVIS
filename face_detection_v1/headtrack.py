import math
import cv2
import itertools
import numpy as np
import time
import mediapipe as mp
import pyautogui
import pydirectinput
import sys

sys.path.append('F:\python\JARVIS')
from Commands import *

msg = ""
distance = []

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True) # refine_landmarks = True => it will have points of iris

PreferredHand = 1 # Which Hand Do You prefer to use for commands [ 0 : left 1 : right ]

wCam, hCam = 640, 480
width, height= pyautogui.size()

Video_Capture = cv2.VideoCapture(0)
Video_Capture.set(3,wCam)
Video_Capture.set(4,hCam)

EyeCenter_Index = [468,473] # [left, right]
IrisRightCorner_Index = [173,263] # [left, right]
EyePosOnScreenValue = [0,0] # [x,y]
PointOfHeadTracking_Index = [168,1] # [nose start, nose tip]

HeadRotationMaxAndMinDist = [[30,70],[7,53],[-30,20]] # [max(x,y), center(x,y), min(x,y)] max is to right or down, center is for center and min is when it is left side or up

MovedMouse = False
Count = 10

coordinatesOfEyeLocation = [[30,4],[5,4],[30,-4],[5,-4]] # eye distance when eye is looking at [Top left, Top Right, Bottom Left, Bottom Right]


def DrawPoint():

    global msg, EyeCenter_Index, distance, MovedMouse, Count,EyePosOnScreenValue
    
    color = (0,0,255)

    for facePoint_Index, facePoint_location in enumerate(face_landmarks.landmark):

        if facePoint_Index in PointOfHeadTracking_Index: # Nose tip and start points #in EyeCenter_Index or facePoint_Index in IrisRightCorner_Index: Pupil Center Points

            x1 = facePoint_location.x * wCam
            y1 = facePoint_location.y * hCam

            center = (int(x1), int(y1)) 

            cv2.circle(frame, center, 2, color, 2)         
            
            if MovedMouse == False:
                MoveMouse()

            if Count <= 0:
                MovedMouse = not MovedMouse
                Count = 4
    
            Count = Count - 1

    cv2.putText(frame, msg, (100, 200), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0),1)

def MoveMouse():
    global msg

    HeadRotationDist = GetDistance(PointOfHeadTracking_Index[0],PointOfHeadTracking_Index[1]) # x and y distance as in how much head rotated
    
    RelPosX = face_landmarks.landmark[PointOfHeadTracking_Index[0]].x * width
    RelPosY = face_landmarks.landmark[PointOfHeadTracking_Index[0]].y * height
    
    # X-axis => Left, Right or Center

    if HeadRotationDist[0] <= HeadRotationMaxAndMinDist[1][0] and HeadRotationDist[0] >= -HeadRotationMaxAndMinDist[1][0]:
        # it is in center
        msg = f"center"

    elif HeadRotationDist[0] <= HeadRotationMaxAndMinDist[0][0] and HeadRotationDist[0] >= HeadRotationMaxAndMinDist[1][0]:
        # right side
        RelPosX = reMap(HeadRotationDist[0],HeadRotationMaxAndMinDist[0][0],HeadRotationMaxAndMinDist[1][0],width,face_landmarks.landmark[PointOfHeadTracking_Index[0]].x * width)
        msg = f"right"
        pass
    
    else:
        # left side
        RelPosX = reMap(HeadRotationDist[0],-HeadRotationMaxAndMinDist[1][0],HeadRotationMaxAndMinDist[2][0],face_landmarks.landmark[PointOfHeadTracking_Index[0]].x * width,0)
        msg = f"left"

    # Y-axis => Up, Down or Center
        
    if HeadRotationDist[1] <= HeadRotationMaxAndMinDist[1][1] + 5 and HeadRotationDist[1] >= HeadRotationMaxAndMinDist[1][1] - 5:
        # it is in center
        msg =  msg + f" center {HeadRotationDist[1]}"

    elif  HeadRotationDist[1] >= HeadRotationMaxAndMinDist[1][1]:
        # Down
        RelPosY = reMap(HeadRotationDist[1],HeadRotationMaxAndMinDist[0][1],HeadRotationMaxAndMinDist[1][1],height,face_landmarks.landmark[PointOfHeadTracking_Index[0]].y * height)
        msg = msg + f" Down {[HeadRotationDist[1]]}"
        pass
    
    else:
        # Up
        RelPosY = reMap(HeadRotationDist[1],HeadRotationMaxAndMinDist[1][1],HeadRotationMaxAndMinDist[2][1],face_landmarks.landmark[PointOfHeadTracking_Index[1]].y * height,0)
        msg = msg + f" Up {[HeadRotationDist[1]]}"

    try:
        pyautogui.moveTo(RelPosX, RelPosY)
    except Exception:
        pass

    '''
    distance = GetDistance(EyeCenter_Index[0], IrisRightCorner_Index[0])

    if EyePosOnScreenValue == [0,0]:
        EyePosOnScreenValue = DetectEyePositionOnScreen()

    if MovedMouse == False:
        # Move Mouse
        try:
            EyePosOnScreen = DetectEyePositionOnScreen()

            msg = str([distance, EyePosOnScreen])
            pyautogui.moveTo(EyePosOnScreen[0], EyePosOnScreen[1])
            MovedMouse = True

        except Exception:
            pass

    if Count <= 0:
        MovedMouse = not MovedMouse
        Count = 4
    
    Count = Count - 1
    
    cv2.putText(frame, msg, (100, 200), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0),1)

    for facePoint_Index, facePoint_location in enumerate(face_landmarks.landmark):

        if facePoint_Index in EyeCenter_Index or facePoint_Index in IrisRightCorner_Index: # Pupil Center Points

            x1 = facePoint_location.x * wCam
            y1 = facePoint_location.y * hCam

            center = (int(x1), int(y1)) 

            cv2.circle(frame, center, 2, color, 2)
    
    '''

def DetectEyePositionOnScreen():
    posX = reMap(-distance[0],-coordinatesOfEyeLocation[3][0],-coordinatesOfEyeLocation[0][0],width,0)
    posY = reMap(distance[1],coordinatesOfEyeLocation[0][1],coordinatesOfEyeLocation[3][1],height,0)
    return [posX,posY]

def GetDistance1(face_landmarks,Landmark1ID, Landmark2Id):

    x1 = int(face_landmarks.landmark[Landmark1ID].x * wCam)
    x2 = int(face_landmarks.landmark[Landmark2Id].x * wCam)
    y1 = int(face_landmarks.landmark[Landmark1ID].y * hCam)
    y2 = int(face_landmarks.landmark[Landmark2Id].y * hCam)

    #point1 = (x1,y1)
    #point2 = (x2,y2)

    #distance = math.dist(point1,point2)

    distanceX = x2 - x1
    distanceY = y2 - y1
    distance = [distanceX, distanceY]
    
    return distance

def GetDistance(Landmark1ID, Landmark2Id):

    x1 = int(face_landmarks.landmark[Landmark1ID].x * wCam)
    x2 = int(face_landmarks.landmark[Landmark2Id].x * wCam)
    y1 = int(face_landmarks.landmark[Landmark1ID].y * hCam)
    y2 = int(face_landmarks.landmark[Landmark2Id].y * hCam)

    #point1 = (x1,y1)
    #point2 = (x2,y2)

    #distance = math.dist(point1,point2)

    distanceX = x2 - x1
    distanceY = y2 - y1
    distance = [distanceX, distanceY]
    
    return distance

while True:
    ret, frame = Video_Capture.read()

    frame = cv2.flip(frame,1)

    results = mp_face_mesh.process(frame)

    LEFT_EYE_INDEXES = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_LEFT_EYE)))
    RIGHT_EYE_INDEXES = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_RIGHT_EYE)))
    IRIS_INDEXES = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_IRISES)))

    if results.multi_face_landmarks: # Face Detected
        for face_no, face_landmarks in enumerate(results.multi_face_landmarks):
            DrawPoint()
            pass

    cv2.imshow("Eye Detection", frame)

    if cv2.waitKey(1) == ord('q'):
       Video_Capture.release()
       cv2.destroyAllWindows()
