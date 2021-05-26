from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter.ttk import Scale
from PIL import ImageTk, Image, ImageGrab


class Tools:
    line_x0, line_y0, line_x1, line_y1 = 0, 0, 0, 0


    def __init__(self):
        self.zoom_in_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/zoom in.png").resize((25, 20), Image.ANTIALIAS))
        self.zoom_in = Button(image=self.zoom_in_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                              relief=RAISED, bd=3, command=lambda: self.zoom_control(1))
        self.zoom_in.place(x=1315, y=600)
        self.zoom_out_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/zoom out.png").resize((25, 20), Image.ANTIALIAS))
        self.zoom_out = Button(image=self.zoom_out_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                               relief=RAISED, bd=3, command=lambda: self.zoom_control(0))
        self.zoom_out.place(x=1275, y=600)
        self.pen_color = "black"
        self.color_fill = LabelFrame(root, bd=5, relief=RIDGE, bg="white")
        self.color_fill.place(x=0, y=0, width=70, height=165)
        colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFD700", "#FF00FF", "#FFC0CB",
                  "#800080", "#00ffd9", "#808080"]
        i = j = 0
        for color in colors:
            Button(self.color_fill, bg=color, bd=2, relief=RIDGE, width=3,
                   command=lambda col=color: self.select_color(col)).grid(row=i, column=j)
            i = i + 1
            if i == 6:
                i = 0
                j = 1
        # CREATING BUTTONS:
        self.eraser_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/eraser.png").resize((28, 20), Image.ANTIALIAS))
        self.eraser_btn = Button(root, image=self.eraser_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=self.eraser)
        self.eraser_btn.place(x=0, y=167)
        self.pencil_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/pencil.png.").resize((24, 20), Image.ANTIALIAS))
        self.pencil_btn = Button(root, image=self.pencil_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=self.pencil)
        self.pencil_btn.place(x=37, y=485)
        self.line_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/line.png").resize((24, 20), Image.ANTIALIAS))
        self.line_but = Button(root, image=self.line_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                               relief=RAISED, bd=3, command=self.draw_line)
        self.line_but.place(x=0, y=485)
        self.colorbox_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/bucket.png").resize((25, 20), Image.ANTIALIAS))
        self.colorbox_btn = Button(root, image=self.colorbox_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                   relief=RAISED, bd=3, command=None)
        self.colorbox_btn.place(x=37, y=167)

        # CREATING SIZE FOR PENCIL AND ERASER
        self.pen_size = LabelFrame(root, bd=5, bg="white", relief=RIDGE)
        self.pen_size.place(x=0, y=260, height=130, width=70)
        self.pen_size1 = Scale(self.pen_size, orient=VERTICAL, from_=50, to=0, length=120)
        self.pen_size1.set(1)
        self.pen_size1.grid(row=0, column=1, padx=15)

    def select_color(self, col):
        self.pen_color = col

    def eraser(self):
        self.pen_color = "white"

    def draw_line(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_line)
        self.canvas.bind("<B1-Motion>", self.moving_line)

    def start_line(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.line_x0 = self.canvas.canvasx(event.x)
        self.line_y0 = self.canvas.canvasy(event.y)
        # Create rectangle
        self.line_id = self.canvas.create_line(
            self.line_x0, self.line_y0, self.line_x0, self.line_y0, fill=self.pen_color, width=self.pen_size1.get(),
            smooth=True, capstyle=ROUND)

    def moving_line(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.line_x1 = self.canvas.canvasx(event.x)
        self.line_y1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.line_id, self.line_x0, self.line_y0, self.line_x1, self.line_y1)

    def stop_line(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.line_x1 = self.canvas.canvasx(event.x)
        self.line_y1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.line_id, self.line_x0, self.line_y0, self.line_x1, self.line_y1)

        self.stack.append(self.line_id)
        self.stack.append('$')

    def pencil(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
