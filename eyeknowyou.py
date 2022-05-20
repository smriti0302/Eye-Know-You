import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import cv2
import pandas as pd
import os
import numpy as np
import face_recognition
from datetime import datetime


class MyLabel(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)        
def existing():
    path = r'C:\Users\shruti\Desktop\python\CS Project\face recognition_resource'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
     
    def markAttendance(name):
        with open('Attendance.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
     
     
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
     
    cap = cv2.VideoCapture(0)
     
    while True:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
     
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
     
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
     
        cv2.imshow('Webcam',img)
        cv2.waitKey(1)

        
def newreg():
    def myClick():
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Registration")
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow("Registration", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = e.get()+".jpg"
                path = r"C:\Users\shruti\Desktop\python\CS Project\face recognition_resource{}".format(img_name)
                cv2.imwrite(path, frame)
                print("{} saved!".format(img_name))
                break
        cam.release()
        cv2.destroyAllWindows()
    root1=Tk()
    lb1=Label(root1, text="New Registration")
    lb1.pack()
    lb2=Label(root1, text="Enter your name:")
    lb2.pack()
    e = Entry(root1, width = 50)
    e.pack()
    e.insert(0,"Enter your name")
    bt1 = Button(root1, text = "Done", command = myClick,bg = "blue",fg = "white")
    bt1.pack()
    root1.mainloop()
root = Tk()
root.title("Eye Know You")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.resizable(width=FALSE, height=FALSE)
root.configure(background='black')
anim = MyLabel(root, 'eyeknowyou_img.gif')
anim.place(x=580, y=150)
b1=Button(root, text="EXIT", command=root.destroy)
b1.place(x=900, y=650)
b2=Button(root, text="NEW USER", command=newreg)
b2.place(x=750, y=650)
b3=Button(root, text="EXISTING USER", command=existing)
b3.place(x=600, y=650)
root.mainloop()
