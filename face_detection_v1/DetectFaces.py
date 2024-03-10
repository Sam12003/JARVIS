import math
import time
import cv2
import face_recognition
import os,sys
import numpy as np

known_face_encodings = []
known_face_names = []
face_names = []

def face_confidence(face_distance, face_match_threshold = 0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'
    
def encode_face():

    global known_face_names,known_face_encodings

    for image in os.listdir(r'face_detection_v1\faces'):
        face_image = face_recognition.load_image_file(fr'face_detection_v1\faces\{image}')
        face_encoding = face_recognition.face_encodings(face_image)[0]

        ImageName = image.split('.')[0]
        
        if ImageName not in known_face_names:
            known_face_names.append(ImageName)
            known_face_encodings.append(face_encoding)

    print(known_face_names)

def Detect_Face(n = 2,show = False):
    video_capture = cv2.VideoCapture(0)
    
    ret, frame = video_capture.read()
    
    small_frame = cv2.resize(frame,(0,0), fx = 0.25, fy = 0.25)
        
    #find all faces
    face_locations = face_recognition.face_locations(small_frame)
    
    face_encodings = face_recognition.face_encodings(small_frame,face_locations)
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
        name = 'Unknown'
        confidence = ''
    
        face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)
        best_match_index = np.argmin(face_distance)
    
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            confidence = face_confidence(face_distance[best_match_index])
    
        face_names.append(f'{name} ({confidence})')
    
    # Display anotation
    for(top,right,bottom,left), fac_name in zip(face_locations,face_names):
        top *= 4
        left *= 4
        right *= 4
        bottom *= 4

    #photo = getcroppedimage(frame)
                     
    if show == True:
        check = showVideo(left,top,bottom,right,fac_name,frame,video_capture,n)
    
    return frame,name,confidence,None

def showVideo(left,top,bottom,right,name,frame,video_capture,n):
    cv2.rectangle(frame, (left,top), (right,bottom), (0,0,255),2)
    cv2.rectangle(frame, (left,bottom - 35), (right,bottom), (0,0,255),-1)
    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255),1)
    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(n) == ord('q'):
       video_capture.release()
       cv2.destroyAllWindows()
       return True

def getcroppedimage(frame):
    # loading the haar case algorithm file into alg variable
    alg = r"haarcascade_frontalface_default.xml"
    # passing the algorithm to OpenCV
    haar_cascade = cv2.CascadeClassifier(alg)
    # loading the image path into file_name variable - replace <INSERT YOUR IMAGE NAME HERE> with the path to your image
    # reading the image
    # creating a black and white version of the image
    gray_img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # detecting the faces
    faces = haar_cascade.detectMultiScale( gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100))

    i = 0
    # for each face detected
    for x, y, w, h in faces:
        # crop the image to select only the face
        cropped_image = frame[y : y + h, x : x + w]
        # loading the target image path into target_file_name variable  - replace <INSERT YOUR TARGET IMAGE NAME HERE> with the path to your target image
        target_file_name = 'stored-faces/' + str(i) + '.jpg'
        cv2.imwrite(
            target_file_name,
            cropped_image,
        )
        i = i + 1;

        try:
            if(cropped_image != None):
                return cropped_image
        except:
            return frame

def Exicute():    
    encode_face()

    while True:
        n = 1
        check = False
        try:
            photo,name,confidence,check = Detect_Face(n, True)
            print(f'name: {name} \nconfidence: {confidence} \n{photo}')
        except Exception:
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()
            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(n) == ord('q'):
                video_capture.release()
                cv2.destroyAllWindows()
            pass
        
        if check == True:
            break

        time.sleep(n)

#Exicute()