from tkinter import *

from PIL import ImageTk, Image
from Module import canvas

root = Tk()


class Shapes:
    rect_x0, rect_y0, rect_x1, rect_y1 = 0, 0, 0, 0
    oval_x0, oval_y0, oval_x1, oval_y1 = 0, 0, 0, 0
    pent_x0, pent_y0 = 0, 0
    hex_x0, hex_y0 = 0, 0
    parallelogram_x0, parallelogram_y0 = 0, 0
    tri_x0, tri_y0 = 0, 0
    rect_id = 0
    oval_id = 0
    line_id = 0
    pentagon_id = 0
    triangle_id = 0
    hexagon_id = 0
    parallelogram_id = 0

    def __init__(self):
        self.rectangle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/shapes/rectangle.png").resize((24, 20),
                                                                                                         Image.ANTIALIAS))
        self.rec = Button(root, image=self.rectangle_img, fg="red", bg="white",
                          font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_rectangle)
        self.rec.place(x=0, y=395)

        self.circle_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/shapes/circle.png").resize((24, 20), Image.ANTIALIAS))
        self.circle_btn = Button(root, image=self.circle_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=self.draw_oval)
        self.circle_btn.place(x=0, y=425)

        self.triangle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/shapes/triangle.png").resize((24, 20),
                                                                                                       Image.ANTIALIAS))
        self.triangle_btn = Button(root, image=self.triangle_img, fg="red", bg="white",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_triangle)
        self.triangle_btn.place(x=37, y=395)

        self.pentagon_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/shapes/pentagon.png").resize((24, 20),
                                                                                                       Image.ANTIALIAS))
        self.pentagon_btn = Button(root, image=self.pentagon_img, fg="red", bg="white",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_pentagon)
        self.pentagon_btn.place(x=37, y=425)
        self.hexagon_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/shapes/hexagon.png").resize((24, 20), Image.ANTIALIAS))
        self.hexagon_btn = Button(root, image=self.hexagon_img, fg="red", bg="white",
                                  font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_hexagon)
        self.hexagon_btn.place(x=0, y=455)
        self.parallelogram_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/shapes/parallelogram.png").resize((24, 20), Image.ANTIALIAS))
        self.parallelogram_btn = Button(root, image=self.parallelogram_img, fg="red", bg="white",
                                        font=("Arial", 10, "bold"), relief=RAISED, bd=3,
                                        command=self.draw_parallelogram)
        self.parallelogram_btn.place(x=37, y=455)

    def draw_rectangle(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<ButtonRelease-1>", self.stop_rect)
        self.canvas.bind("<B1-Motion>", self.moving_rect)

    def start_rect(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rect_x0 = self.canvas.canvasx(event.x)
        self.rect_y0 = self.canvas.canvasy(event.y)
        # Create rectangle
        self.rect_id = self.canvas.create_rectangle(
            self.rect_x0, self.rect_y0, self.rect_x0, self.rect_y0, outline=self.pen_color,
            width=self.pen_size1.get())

    def moving_rect(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rect_x1 = self.canvas.canvasx(event.x)
        self.rect_y1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rect_id, self.rect_x0, self.rect_y0, self.rect_x1, self.rect_y1)

    def stop_rect(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rect_x1 = self.canvas.canvasx(event.x)
        self.rect_y1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rect_id, self.rect_x0, self.rect_y0, self.rect_x1, self.rect_y1)

        self.stack.append(self.rect_id)
        self.stack.append('$')

    def draw_oval(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_oval)
        self.canvas.bind("<ButtonRelease-1>", self.stop_oval)
        self.canvas.bind("<B1-Motion>", self.moving_oval)

    def start_oval(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.oval_x0 = self.canvas.canvasx(event.x)
        self.oval_y0 = self.canvas.canvasy(event.y)
        # Create oval
        self.oval_id = self.canvas.create_oval(
            self.oval_x0, self.oval_y0, self.oval_x0, self.oval_y0, outline=self.pen_color,
            width=self.pen_size1.get())

    def moving_oval(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.oval_x1 = self.canvas.canvasx(event.x)
        self.oval_y1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.oval_id, self.oval_x0, self.oval_y0, self.oval_x1, self.oval_y1)

    def stop_oval(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.oval_x1 = self.canvas.canvasx(event.x)
        self.oval_y1 = self.canvas.canvasy(event.y)
        # Modify oval x1, y1 coordinates
        self.canvas.coords(self.oval_id, self.oval_x0, self.oval_y0, self.oval_x1, self.oval_y1)

        self.stack.append(self.oval_id)
        self.stack.append('$')

    def draw_triangle(self):
        self.triangle_id = None
        self.canvas.bind("<Button-1>", self.start_triangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_triangle)
        self.canvas.bind("<B1-Motion>", self.moving_triangle)

    def start_triangle(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.tri_x0 = self.canvas.canvasx(event.x)
        self.tri_y0 = self.canvas.canvasy(event.y)
        # Create triangle
        self.triangle_id = self.canvas.create_polygon(self.tri_x0, self.tri_y0,
                                                      self.tri_x0 - (event.x - self.tri_x0), event.y, event.x,
                                                      event.y, outline=self.pen_color, width=self.pen_size1.get(),
                                                      fill='white')

    def moving_triangle(self, event):
        # Modify triangle x1, y1 coordinates
        self.canvas.coords(self.triangle_id, self.tri_x0, self.tri_y0, self.tri_x0 - (event.x - self.tri_x0),
                           event.y, event.x, event.y)

    def stop_triangle(self, event):
        # Modify triangle x1, y1 coordinates
        self.canvas.coords(self.triangle_id, self.tri_x0, self.tri_y0, self.tri_x0 - (event.x - self.tri_x0),
                           event.y, event.x, event.y)
        self.stack.append(self.triangle_id)
        self.stack.append('$')

    def draw_pentagon(self):
        self.canvas.bind("<Button-1>", self.start_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.stop_pentagon)
        self.canvas.bind("<B1-Motion>", self.moving_pentagon)

    def start_pentagon(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.pent_x0 = self.canvas.canvasx(event.x)
        self.pent_y0 = self.canvas.canvasy(event.y)
        # Create pentagon
        self.pentagon_id = self.canvas.create_polygon(self.pent_x0, self.pent_y0, int(self.pent_x0), event.y,
                                                      event.x, event.y, int(event.x), self.pent_y0,
                                                      (self.pent_x0 + event.x) / 2, self.pent_y0 - 20,
                                                      outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_pentagon(self, event):
        # Modify pentagon x1, y1 coordinates
        self.canvas.coords(self.pentagon_id, self.pent_x0, self.pent_y0, int(self.pent_x0), event.y, event.x, event.y,
                           int(event.x), self.pent_y0, (self.pent_x0 + event.x) / 2,
                           self.pent_y0 - 20)

    def stop_pentagon(self, event):
        self.canvas.coords(self.pentagon_id, self.pent_x0, self.pent_y0, int(self.pent_x0), event.y, event.x, event.y,
                           int(event.x), self.pent_y0, (self.pent_x0 + event.x) / 2,
                           self.pent_y0 - 20)
        self.stack.append(self.pentagon_id)
        self.stack.append('$')

    def draw_hexagon(self):
        self.canvas.bind("<Button-1>", self.start_hexagon)
        self.canvas.bind("<ButtonRelease-1>", self.stop_hexagon)
        self.canvas.bind("<B1-Motion>", self.moving_hexagon)

    def start_hexagon(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.hex_x0 = self.canvas.canvasx(event.x)
        self.hex_y0 = self.canvas.canvasy(event.y)
        # Create hexagon
        self.hexagon_id = self.canvas.create_polygon(self.hex_x0, self.hex_y0, int(self.hex_x0), event.y,
                                                     (int(self.hex_x0) + int(event.x)) / 2, int(event.y) + 50,
                                                     event.x, event.y, int(event.x), self.hex_y0,
                                                     (self.hex_x0 + event.x) / 2, self.hex_y0 - 50,
                                                     outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_hexagon(self, event):
        # Modify hexagon  x1, y1 coordinates
        self.canvas.coords(self.hexagon_id, self.hex_x0, self.hex_y0, int(self.hex_x0), event.y,
                           (int(self.hex_x0) + int(event.x)) / 2,
                           int(event.y) + 50, event.x, event.y, int(event.x), self.hex_y0,
                           (self.hex_x0 + event.x) / 2, self.hex_y0 - 50)

    def stop_hexagon(self, event):
        self.canvas.coords(self.hexagon_id, self.hex_x0, self.hex_y0, int(self.hex_x0), event.y,
                           (int(self.hex_x0) + int(event.x)) / 2,
                           int(event.y) + 50, event.x, event.y, int(event.x), self.hex_y0,
                           (self.hex_x0 + event.x) / 2, self.hex_y0 - 50)
        self.stack.append(self.hexagon_id)
        self.stack.append('$')

    def draw_parallelogram(self):
        self.canvas.bind("<Button-1>", self.start_parallelogram)
        self.canvas.bind("<ButtonRelease-1>", self.stop_parallelogram)
        self.canvas.bind("<B1-Motion>", self.moving_parallelogram)

    def start_parallelogram(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.parallelogram_x0 = self.canvas.canvasx(event.x)
        self.parallelogram_y0 = self.canvas.canvasy(event.y)
        # Create parallelogram
        self.parallelogram_id = self.canvas.create_polygon(self.parallelogram_x0, self.parallelogram_y0,
                                                           int(self.parallelogram_x0) + 30, event.y,
                                                           event.x, event.y, int(event.x) - 30, self.parallelogram_y0,
                                                           outline=self.pen_color, width=self.pen_size1.get(),
                                                           fill='white')

    def moving_parallelogram(self, event):
        # Modify parallelogram x1, y1 coordinates
        self.canvas.coords(self.parallelogram_id, self.parallelogram_x0, self.parallelogram_y0,
                           int(self.parallelogram_x0) + 30, event.y, event.x, event.y, int(event.x) - 30,
                           self.parallelogram_y0)

    def stop_parallelogram(self, event):
        # Modify parallelogram x1, y1 coordinates
        self.canvas.coords(self.parallelogram_id, self.parallelogram_x0, self.parallelogram_y0,
                           int(self.parallelogram_x0) + 30, event.y, event.x, event.y, int(event.x) - 30,
                           self.parallelogram_y0)
        self.stack.append(self.parallelogram_id)
        self.stack.append('$')


shapes = Shapes()
root.mainloop()
