from tkinter import *
from tkinter import colorchooser
from doodle import root


class Canvas:
    x_start, y_start = 0, 0

    def __init__(self):
        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=600, width=1000)
        self.canvas.place(x=80, y=0)

        self.stack = []
        self.item = None

        self.pen_color = "black"

        self.pen_size = LabelFrame(root, bd=5, bg="white", relief=RIDGE)
        self.pen_size.place(x=0, y=260, height=130, width=70)
        self.pen_size1 = Scale(self.pen_size, orient=VERTICAL, from_=50, to=0, length=120)
        self.pen_size1.set(1)
        self.pen_size1.grid(row=0, column=1, padx=15)

        self.status_bar = Label(bd=5, relief=RIDGE, font='Times 15 bold', bg='white', fg='black', anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

    def paint_app(self, event):
        if self.x_start and self.y_start:
            self.stack.append(self.canvas.create_line(self.x_start, self.y_start, event.x, event.y,
                                                      width=self.pen_size1.get(), fill=self.pen_color,
                                                      capstyle=ROUND, smooth=True))

        self.x_start = event.x
        self.y_start = event.y

    def reset(self):
        self.x_start = None
        self.y_start = None
        self.stack.append('#')

    def coordinates(self, event):
        self.status_bar['text'] = f'{event.x},{event.y}px'

    def canvas_bg(self):
        color = colorchooser.askcolor()
        self.canvas.configure(background=color[1])
