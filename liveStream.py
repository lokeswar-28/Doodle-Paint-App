from tkinter import *
import cv2
import PIL
from PIL import ImageTk, Image, ImageGrab

import globals


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, globals.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, globals.height)
lmain = Label(globals.root)
lmain.pack(side="right")
lmain.place(x=1000, y=0)

def show_frame():
    _, frame = cap.read()
    if _:
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)