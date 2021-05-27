from tkinter import *
from Module.canvas import Canvas
from doodle import root


class Tools:
    line_x0, line_y0, line_x1, line_y1 = 0, 0, 0, 0
    line_id = 0

    def __init__(self):

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

        # CREATING SIZE FOR PENCIL AND ERASER
        self.pen_size = LabelFrame(root, bd=5, bg="white", relief=RIDGE)
        self.pen_size.place(x=0, y=260, height=130, width=70)
        self.pen_size1 = Scale(self.pen_size, orient=VERTICAL, from_=50, to=0, length=120)
        self.pen_size1.set(1)
        self.pen_size1.grid(row=0, column=1, padx=15)

        self.canvas = Button(root, text="Canvas", bd=4, bg="white", width=8, relief=RIDGE, command=Canvas.canvas_bg)
        self.canvas.place(x=0, y=227)
        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=600, width=1000)
        self.canvas.place(x=80, y=0)

        self.stack = []
        self.item = None

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
        self.canvas.bind("<B1-Motion>", Canvas.paint_app)
        self.canvas.bind("<ButtonRelease-1>", Canvas.reset)

    def zoom_control(self, event):  # For Zoom in and Zoom out
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)

        elif event == 1:
            self.canvas.scale("all", 550, 350, 1.1, 1.1)
        else:
            self.canvas.scale("all", 550, 350, 1.1, 1.1)

    def undo(self, event):

        try:
            self.item = self.stack.pop()

            if self.item == '$':  # For undoing figures like rectangle, oval, circle, square, straight lines.
                self.item = self.stack.pop()
                self.canvas.delete(self.item)

            elif self.item == '#':
                self.item = self.stack.pop()
                while self.item != '#' and self.item != '$':
                    self.canvas.delete(self.item)
                    if len(self.stack) == 0:
                        break
                    self.item = self.stack.pop()

                if self.item == '#' or self.item == '$':
                    self.stack.append(self.item)
        except IndexError:
            pass
