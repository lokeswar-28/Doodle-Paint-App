from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Scale
from PIL import ImageTk, Image, ImageGrab
from tkinter import colorchooser


root = Tk()
root.attributes("-fullscreen", False)
root.title("DOODLE")
Icon = PhotoImage(file="doodle.png")
root.iconphoto(False, Icon)


class Paint:
    font = StringVar()
    text = IntVar()
    bold = IntVar()
    italic = IntVar()
    x_start, y_start, x_final, y_final = 0, 0, 0, 0
    rect_id = 0
    oval_id = 0
    line_id = 0
    pentagon_id = 0
    triangle_id = 0
    hexagon_id = 0
    parallelogram_id = 0

    @staticmethod
    def quit():
        root.quit()

    @staticmethod
    def about():
        messagebox.showinfo('DOODLE', 'Go to the help in the main window')

    def open_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
                                              ("jpeg files", "*.jpg"), ("png files", "*.png")))
        image = Image.open(filename)
        image.save("Temp.png", "png")
        self.canvas.create_image(3, 3, image=self.file_to_open, anchor=NW)

    def save_file(self):
        file = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(
                                                ("jpeg files", "*.jpg"), ("png files", "*.png")))
        if file:
            x = root.winfo_rootx() + self.canvas.winfo_x()
            y = root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file + '.png')
            ImageGrab.grab().crop((x, y, x1, y1)).save(file + '.jpg')

    def menu_bar(self):
        menu = Menu(root)
        # FILE MENU
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="📂 Open", command=self.open_file)
        file_menu.add_command(label="📥 Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Quit", command=self.quit)
        menu.add_cascade(label="🗂 File", menu=file_menu)

        # FONT MENU:
        font_menu = Menu(menu, tearoff=0)
        type_submenu = Menu(font_menu)
        type_submenu.add_radiobutton(label="Times", variable=self.font)
        type_submenu.add_radiobutton(label="Courier", variable=self.font)
        type_submenu.add_radiobutton(label="Ariel", variable=self.font)
        font_menu.add_cascade(label="Font style", menu=type_submenu)

        size_submenu = Menu(font_menu)
        size_submenu.add_radiobutton(label="🛑 10", variable=self.text)
        size_submenu.add_radiobutton(label="🛑 15", variable=self.text)
        size_submenu.add_radiobutton(label="🛑 20", variable=self.text)
        size_submenu.add_radiobutton(label="🛑 25", variable=self.text)
        font_menu.add_cascade(label="Font size", menu=size_submenu)
        font_menu.add_checkbutton(label="Bold", variable=self.bold, onvalue=1, offvalue=0)
        menu.add_cascade(label="✏ Font", menu=font_menu)

        # EDIT MENU
        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menu.add_cascade(label="✒ Edit", menu=edit_menu)

        # HELP MENU
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="⁉ About", command=self.about)
        menu.add_cascade(label="❓ Help", menu=help_menu)

        root.config(menu=menu)

    def __init__(self):
        self.file_to_open = PhotoImage(file="Temp.png")
        self.my_label = Label(bd=5, relief=RIDGE, font='Times 15 bold', bg='white', fg='black', anchor=W)
        self.my_label.pack(side=BOTTOM, fill=X)
        self.menu_bar()
        self.pen_color = "black"
        self.color_fill = LabelFrame(root, text="Color", font=("Times", 15, "bold"), bd=5, relief=RIDGE, bg="white")
        self.color_fill.place(x=0, y=0, width=70, height=185)
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
            Image.open("Pictures/eraser.png").resize((28, 20), Image.ANTIALIAS))
        self.eraser_btn = Button(root, image=self.eraser_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=self.eraser)
        self.eraser_btn.place(x=0, y=187)
        self.pencil_img = ImageTk.PhotoImage(
            Image.open("Pictures/pencil1.png.").resize((20, 20), Image.ANTIALIAS))
        self.pencil_btn = Button(root, image=self.pencil_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=self.pencil)
        self.pencil_btn.place(x=37, y=545)
        self.line_img = ImageTk.PhotoImage(
            Image.open("Pictures/line.png").resize((20, 20), Image.ANTIALIAS))
        self.line_but = Button(root, image=self.line_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                               relief=RAISED, bd=3, command=self.draw_line)
        self.line_but.place(x=0, y=545)
        self.colorbox_img = ImageTk.PhotoImage(
            Image.open("Pictures/bucket.jpg").resize((25, 20), Image.ANTIALIAS))
        self.colorbox_btn = Button(root, image=self.colorbox_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                   relief=RAISED, bd=3, command=None)
        self.colorbox_btn.place(x=37, y=187)
        self.clear = Button(root, text="Clear", bd=4, bg="white", width=8, relief=RIDGE,
                            command=lambda: self.canvas.delete("all"))
        self.clear.place(x=0, y=217)
        self.canvas = Button(root, text="Canvas", bd=4, bg="white", width=8, relief=RIDGE, command=self.canvas_bg)
        self.canvas.place(x=0, y=247)
        # CREATING SIZE FOR PENCIL AND ERASER
        self.pen_size = LabelFrame(root, text="Size", bd=5, bg="white", font=("Times", 15, "bold"), relief=RIDGE)
        self.pen_size.place(x=0, y=280, height=150, width=70)
        self.pen_size1 = Scale(self.pen_size, orient=VERTICAL, from_=50, to=0, length=120)
        self.pen_size1.set(1)
        self.pen_size1.grid(row=0, column=1, padx=15)
        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=600, width=1000)
        self.canvas.place(x=80, y=0)
        self.shapes = Label(root, text="Shapes", bd=4, bg="white", width=8, relief=RIDGE, command=None)
        self.shapes.place(x=0, y=430)
        self.rectangle_img = ImageTk.PhotoImage(Image.open("Pictures/rectangle.jpg").resize((20, 20), Image.ANTIALIAS))
        self.rec = Button(root, image=self.rectangle_img, fg="red", bg="white",
                          font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_rectangle)
        self.rec.place(x=0, y=455)

        self.circle_img = ImageTk.PhotoImage(
            Image.open("Pictures/circle.png").resize((20, 20), Image.ANTIALIAS))
        self.circle_btn = Button(root, image=self.circle_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=self.draw_oval)
        self.circle_btn.place(x=0, y=485)

        assert isinstance(Image.open("Pictures/triangle.jpg").resize, object)
        self.triangle_img = ImageTk.PhotoImage(Image.open("Pictures/triangle.jpg").resize((20, 20), Image.ANTIALIAS))
        self.triangle_btn = Button(root, image=self.triangle_img, fg="red", bg="white",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_triangle)
        self.triangle_btn.place(x=37, y=455)

        self.pentagon_img = ImageTk.PhotoImage(Image.open("Pictures/pentagon.png").resize((20, 20), Image.ANTIALIAS))
        self.pentagon_btn = Button(root, image=self.pentagon_img, fg="red", bg="white",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_pentagon)
        self.pentagon_btn.place(x=37, y=485)
        self.hexagon_img = ImageTk.PhotoImage(Image.open("Pictures/hexagon.png").resize((20, 20), Image.ANTIALIAS))
        self.hexagon_btn = Button(root, image=self.hexagon_img, fg="red", bg="white",
                                  font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_hexagon)
        self.hexagon_btn.place(x=0, y=515)
        self.parallelogram_img = ImageTk.PhotoImage(
            Image.open("Pictures/parallelogram.png").resize((20, 20), Image.ANTIALIAS))
        self.parallelogram_btn = Button(root, image=self.parallelogram_img, fg="red", bg="white",
                                        font=("Arial", 10, "bold"), relief=RAISED, bd=3,
                                        command=self.draw_parallelogram)
        self.parallelogram_btn.place(x=37, y=515)

        # mouse drag
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.canvas.bind("<Motion>", self.coordinates)

    def paint_app(self, event):
        x_start, y_start = (event.x - 2), (event.y - 2)
        x_final, y_final = (event.x + 2), (event.y + 2)

        self.canvas.create_oval(x_start, y_start, x_final, y_final, outline=self.pen_color,
                                fill=self.pen_color, width=self.pen_size1.get())

    def select_color(self, col):
        self.pen_color = col

    def eraser(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.pen_color = "white"

    def coordinates(self, event):
        self.my_label['text'] = f'Cursor coordinates : ({event.x},{event.y})'

    def canvas_bg(self):
        color = colorchooser.askcolor()
        self.canvas.configure(background=color[1])

    def draw_rectangle(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<ButtonRelease-1>", self.stop_rect)
        self.canvas.bind("<B1-Motion>", self.moving_rect)

    def start_rect(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create rectangle
        self.rect_id = self.canvas.create_rectangle(
            self.x_start, self.y_start, self.x_start, self.y_final, outline=self.pen_color, width=self.pen_size1.get())

    def moving_rect(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rect_id, self.x_start, self.y_start,
                           self.x_final, self.y_final)

    def stop_rect(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.rect_id, self.x_start, self.y_start,
                           self.x_final, self.y_final)

    def draw_oval(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_oval)
        self.canvas.bind("<ButtonRelease-1>", self.stop_oval)
        self.canvas.bind("<B1-Motion>", self.moving_oval)

    def start_oval(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create rectangle
        self.oval_id = self.canvas.create_oval(
            self.x_start, self.y_start, self.x_final, self.y_final, outline=self.pen_color, width=self.pen_size1.get())

    def moving_oval(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.oval_id, self.x_start, self.y_start,
                           self.x_final, self.y_final)

    def stop_oval(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates
        self.canvas.coords(self.oval_id, self.x_start, self.y_start,
                           self.x_final, self.y_final)

    def draw_line(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_line)
        self.canvas.bind("<B1-Motion>", self.moving_line)

    def start_line(self, event):

        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create line
        self.line_id = self.canvas.create_line(self.x_start, self.y_start, self.x_start, self.y_start,
                                               fill=self.pen_color, width=self.pen_size1.get(), smooth=True,
                                               capstyle=ROUND)

    def moving_line(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify line x0, y0 coordinates
        self.canvas.coords(self.line_id, self.x_start, self.y_start, self.x_final, self.y_final)

    def stop_line(self, event):
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify line x1, y1 coordinates
        self.canvas.coords(self.line_id, self.x_start, self.y_start, self.x_final, self.y_final)

    def draw_triangle(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_triangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_triangle)
        self.canvas.bind("<B1-Motion>", self.moving_triangle)

    def start_triangle(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create triangle
        self.triangle_id = self.canvas.create_polygon(self.x_start, self.y_start,
                                                      self.x_start - (event.x - self.x_start), event.y, event.x,
                                                      event.y, outline=self.pen_color, width=self.pen_size1.get(),
                                                      fill='white')

    def moving_triangle(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify triangle x1, y1 coordinates
        self.canvas.coords(self.triangle_id, self.x_start, self.y_start, self.x_start - (event.x - self.x_start),
                           event.y, event.x, event.y)

    def stop_triangle(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify triangle x1, y1 coordinates
        self.canvas.coords(self.triangle_id, self.x_start, self.y_start, self.x_start - (event.x - self.x_start),
                           event.y, event.x, event.y)

    def draw_pentagon(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.stop_pentagon)
        self.canvas.bind("<B1-Motion>", self.moving_pentagon)

    def start_pentagon(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create pentagon
        self.pentagon_id = self.canvas.create_polygon(self.x_start, self.y_start, int(self.x_start), event.y,
                                                      event.x, event.y, int(event.x), self.y_start,
                                                      (self.x_start + event.x) / 2, self.y_start - 20,
                                                      outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_pentagon(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify pentagon x1, y1 coordinates
        self.canvas.coords(self.pentagon_id, self.x_start, self.y_start, int(self.x_start), event.y, event.x, event.y,
                           int(event.x), self.y_start, (self.x_start + event.x) / 2,
                           self.y_start - 20)

    def stop_pentagon(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify pentagon x1, y1 coordinates
        self.canvas.coords(self.pentagon_id, self.x_start, self.y_start, int(self.x_start), event.y, event.x, event.y,
                           int(event.x), self.y_start, (self.x_start + event.x) / 2,
                           self.y_start - 20)

    def draw_hexagon(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_hexagon)
        self.canvas.bind("<ButtonRelease-1>", self.stop_hexagon)
        self.canvas.bind("<B1-Motion>", self.moving_hexagon)

    def start_hexagon(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create hexagon
        self.hexagon_id = self.canvas.create_polygon(self.x_start, self.y_start, int(self.x_start), event.y,
                                                     (int(self.x_start) + int(event.x)) / 2, int(event.y) + 50,
                                                     event.x, event.y, int(event.x), self.y_start,
                                                     (self.x_start + event.x) / 2, self.y_start - 50,
                                                     outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_hexagon(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify hexagon  x1, y1 coordinates
        self.canvas.coords(self.hexagon_id, self.x_start, self.y_start, int(self.x_start), event.y,
                           (int(self.x_start) + int(event.x)) / 2,
                           int(event.y) + 50, event.x, event.y, int(event.x), self.y_start,
                           (self.x_start + event.x) / 2, self.y_start - 50)

    def stop_hexagon(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify hexagon x1, y1 coordinates
        self.canvas.coords(self.hexagon_id, self.x_start, self.y_start, int(self.x_start), event.y,
                           (int(self.x_start) + int(event.x)) / 2,
                           int(event.y) + 50, event.x, event.y, int(event.x), self.y_start,
                           (self.x_start + event.x) / 2, self.y_start - 50)

    def draw_parallelogram(self):

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.start_parallelogram)
        self.canvas.bind("<ButtonRelease-1>", self.stop_parallelogram)
        self.canvas.bind("<B1-Motion>", self.moving_parallelogram)

    def start_parallelogram(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.x_start = self.canvas.canvasx(event.x)
        self.y_start = self.canvas.canvasy(event.y)
        # Create parallelogram
        self.parallelogram_id = self.canvas.create_polygon(self.x_start, self.y_start, int(self.x_start) + 30, event.y,
                                                           event.x, event.y, int(event.x) - 30, self.y_start,
                                                           outline=self.pen_color, width=self.pen_size1.get(),
                                                           fill='white')

    def moving_parallelogram(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify parallelogram x1, y1 coordinates
        self.canvas.coords(self.parallelogram_id, self.x_start, self.y_start, int(self.x_start) + 30,
                           event.y, event.x, event.y, int(event.x) - 30, self.y_start)

    def stop_parallelogram(self, event):
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.x_final = self.canvas.canvasx(event.x)
        self.y_final = self.canvas.canvasy(event.y)
        # Modify parallelogram x1, y1 coordinates
        self.canvas.coords(self.parallelogram_id, self.x_start, self.y_start, int(self.x_start) + 30,
                           event.y, event.x, event.y, int(event.x) - 30, self.y_start)

    def pencil(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint_app)


paint = Paint()
root.mainloop()
