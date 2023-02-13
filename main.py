#!/usr/bin/env python3

import face_recognition
import os
import cv2
import numpy as np
import pywhatkit
from boltiot import Bolt

path='ImageAttendance'
images = []
classNames = []
mylist = os.listdir(path)
api_key = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
device_id  = "BOLT1234"
mybolt = Bolt(api_key, device_id)
response = mybolt.serialBegin('9600')
for cl in mylist:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findencodings(images):
    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

encodeliseknown=findencodings(images)
print("Encoding complete")

cap=cv2.VideoCapture(0)

while True:
    success, img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    facesCurFrame=face_recognition.face_locations(imgS)
    encodesCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches=face_recognition.compare_faces(encodeliseknown,encodeFace)
        faceDis=face_recognition.face_distance(encodeliseknown,encodeFace)
        #print(faceDis)
        matcheIndex=np.argmin(faceDis)

        if matches[matcheIndex]:
            name=classNames[matcheIndex].upper()
            print(name)
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        
        else:
            response = mybolt.serialWrite('Hello')
            pywhatkit.sendwhatmsg_instantly( phone_no="+919380465853", message="Stranger detected")


    cv2.imshow('webcam',img)
    cv2.waitKey(1)
