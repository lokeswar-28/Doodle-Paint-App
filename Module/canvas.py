from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter.ttk import Scale
from PIL import ImageTk, Image, ImageGrab
from tkinter import colorchooser

root = Tk()


class Canvas:
    x_start, y_start = 0, 0

    def __init__(self):
        self.clear = Button(root, text="Clear", bd=4, bg="white", width=8, relief=RIDGE,
                            command=lambda: self.canvas.delete("all"))
        self.clear.place(x=0, y=197)
        self.canvas = Button(root, text="Canvas", bd=4, bg="white", width=8, relief=RIDGE, command=self.canvas_bg)
        self.canvas.place(x=0, y=227)
        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=600, width=1000)
        self.canvas.place(x=80, y=0)
        self.xsb = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))
        self.xsb.pack(side=BOTTOM, fill=X)
        self.ysb.pack(side=RIGHT, fill=Y)

        # mouse drag
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Motion>", self.coordinates)

    def paint_app(self, event):
        if self.x_start and self.y_start:
            self.stack.append(self.canvas.create_line(self.x_start, self.y_start, event.x, event.y,
                                    width=self.pen_size1.get(), fill=self.pen_color,
                                    capstyle=ROUND, smooth=True))

        self.x_start = event.x
        self.y_start = event.y

    def reset(self, event):
        self.x_start = None
        self.y_start = None
        self.stack.append('#')

    def coordinates(self, event):
        self.status_bar['text'] = f'{event.x},{event.y}px'

    def canvas_bg(self):
        color = colorchooser.askcolor()
        self.canvas.configure(background=color[1])
