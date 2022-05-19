import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import pandas as pd
import xlwt 
from xlwt import Workbook
import os
# Workbook is created 
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1') 


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
                img_name ="unknown"+".png"
                path = r"C:\Users\Sivakumar\Desktop\Face recog attendance\opencv-face-recognition\dataset\p1.png"
                cv2.imwrite(path,frame)
                cv2.waitKey(0)
                print("{} saved!".format(img_name))
                break
        cam.release()
        cv2.destroyAllWindows()
    
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
                img_name = e.get()+".png"
                path = r"C:\Users\Sivakumar\Desktop\Face recog attendance\opencv-face-recognition\images\{}".format(e.get()+".png")
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
