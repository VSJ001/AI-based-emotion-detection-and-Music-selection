import cv2
import time
from deepface import DeepFace
import tkinter as tk

class Face:
    def opencam(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        cap.set(3,700)
        cap.set(4,720)

        while cap.isOpened():
            ret,frame = cap.read()
            result = DeepFace.analyze(img_path=frame,actions=['emotion'],enforce_detection=False)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.1,4)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            self.emotion = result[0]['dominant_emotion']
            txt = str(self.emotion)
            cv2.putText(frame,txt,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
            #cv2.imshow('frame',frame)
            time.sleep(5)
            break
        
        cap.release()
        cv2.destroyAllWindows()
        return self.emotion


