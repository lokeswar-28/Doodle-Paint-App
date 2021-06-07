from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter.ttk import Scale
import PIL
from PIL import ImageTk, Image, ImageGrab
from tkinter import colorchooser
import time
import cv2

root = Tk()
root.geometry("1150x750")
root.title("DOODLE")
Icon = PhotoImage(file="Utils/Pictures/Icon/doodle.png")
root.iconphoto(True, Icon)
root.config(cursor="tcross")
width, height = 365, 350
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
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


show_frame()


class Paint:
    # Initialisation
    x_start, y_start = 0, 0
    x_final, y_final = 0, 0
    line_x0, line_y0, line_x1, line_y1 = 0, 0, 0, 0
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
    file_to_open: PhotoImage
    menu_img_container = []
    about_img = []
    selection_id = 0
    temp = []
    cut_copy_img = []
    counter = -1
    img_label_all = []
    heading, txt, entry, top = None, None, None, None
    des_label_all = []

    def new(self):
        take = messagebox.askyesno("New Window Conformation", "Do you really want to open new Window?")
        root.title("Doodle" + "-----" + "New Window")
        if take is True:
            self.canvas.delete("all")

    def open_file(self):
        try:
            filename = filedialog.askopenfilename(initialdir="/", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
            image = Image.open(filename)
            image.save("Temp.png", "png")
            self.file_to_open = PhotoImage(file="Temp.png")
            self.canvas.delete("all")
            self.canvas.create_image(3, 3, image=self.file_to_open, anchor=NW)
        except AttributeError:
            pass

    def save_file(self, _=None):
        file = filedialog.asksaveasfilename(initialdir="/", filetypes=(
            ("jpeg files", "*.jpg"), ("png files", "*.png")))
        if file:
            x = root.winfo_rootx() + self.canvas.winfo_x()
            y = root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file + '.png')
            ImageGrab.grab().crop((x, y, x1, y1)).save(file + '.jpg')

    @staticmethod
    def quit():
        take = messagebox.askyesno("Quit Conformation", "Do you really want to quit?")
        if take is True:
            root.quit()

    def undo(self, _=None):
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

    def cut(self, _=None):  # Cut the selected region
        self.copy(1)
        self.delete_selected_region(False)
        self.canvas.unbind("<B1-Motion>")

    def copy(self, _=None):  # Copy the selected region
        try:
            self.canvas.itemconfig(self.temp[len(self.temp) - 1], outline="white")
            time.sleep(0.0001)
            self.canvas.update()
            x1 = root.winfo_rootx() + self.canvas.winfo_x()
            y1 = root.winfo_rooty() + self.canvas.winfo_y()
            ImageGrab.grab().crop((x1 + self.rect_x0, y1 + self.rect_y0, x1 + self.rect_x1, y1 + self.rect_y1)).save(
                "cutting.png")
            self.counter += 1
            self.reset_rectangle()
        except BaseException:
            messagebox.showerror("Cut error")

    def paste(self, _=None):  # Paste the region keep in clipboard
        messagebox.showinfo('Paste', ''' 📣 Please set the mouse pointer then click the left button 📣''')
        self.cut_copy_img.append(ImageTk.PhotoImage(Image.open("cutting.png")))
        self.canvas.bind('<Button-1>', self.place)
        self.canvas.bind("<Motion>", self.coordinates)
        self.canvas.bind('<Button-3>', self.cancel)

    def place(self, event):
        take = self.canvas.create_image(event.x, event.y, image=self.cut_copy_img[self.counter])
        self.stack.append(take)
        self.stack.append('$')

    def menu_bar(self):
        menu = Menu(root)
        menu_img = ["open.png", "save.png", "exit.png", "undo.png", "cut.png", "copy.png", "paste.png", "text.png", "about.png", "new.png"]
        for i in range(10):
            self.menu_img_container.append(i)
            self.menu_img_container[i] = ImageTk.PhotoImage(
                Image.open("Utils/Pictures/Menu_bar/" + menu_img[i]).resize((30, 30), Image.ANTIALIAS))
        # FILE MENU
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label=" New", command=self.new, image=self.menu_img_container[9], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        file_menu.add_command(label="Open", command=self.open_file, image=self.menu_img_container[0], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S", image=self.menu_img_container[1], compound=LEFT, background="white", foreground="blue",
                              font=("Arial", 10, "bold"), activebackground="blue", activeforeground="white")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit, image=self.menu_img_container[2], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        menu.add_cascade(label="🗂 File", menu=file_menu)

        # EDIT MENU
        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z", image=self.menu_img_container[3], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+C", image=self.menu_img_container[4], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+X", image=self.menu_img_container[5], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V", image=self.menu_img_container[6], compound=LEFT, background="white", foreground="blue",
                              font=("Arial", 10, "bold"), activebackground="blue", activeforeground="white")
        menu.add_cascade(label="✒ Edit", menu=edit_menu)

        # TEXT MENU
        text_menu = Menu(menu, tearoff=0)
        text_menu.add_command(label="Text", command=self.add_text, image=self.menu_img_container[7], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        menu.add_cascade(label="🖊 Text", menu=text_menu)

        # HELP MENU
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.about, image=self.menu_img_container[8], compound=LEFT, background="white", foreground="blue", font=("Arial", 10, "bold"),
                              activebackground="blue", activeforeground="white")
        menu.add_cascade(label="❓ Help", menu=help_menu)

        root.config(menu=menu)
        root.bind("<Control-z>", self.undo)
        root.bind("<Control-s>", self.save_file)
        root.bind("<Control-x>", self.cut)
        root.bind("<Control-c>", self.copy)
        root.bind("<Control-v>", self.paste)

    def __init__(self):
        self.stack = []
        self.item = None
        self.status_bar = Label(bd=5, relief=RIDGE, font='Times 15 bold', bg='white', fg='black', anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.zoom_in_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/zoom in.png").resize((25, 20), Image.ANTIALIAS))
        self.zoom_in = Button(image=self.zoom_in_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.zoom_control(1))
        self.zoom_in.place(x=1315, y=600)
        self.zoom_out_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/zoom out.png").resize((25, 20), Image.ANTIALIAS))
        self.zoom_out = Button(image=self.zoom_out_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=lambda: self.zoom_control(0))
        self.zoom_out.place(x=1275, y=600)
        self.menu_bar()
        self.pen_color = "black"
        self.color_fill = LabelFrame(root, bd=5, relief=RIDGE, bg="blue")
        self.color_fill.place(x=0, y=0, width=70, height=165)
        colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFD700", "#FF00FF", "#FFC0CB", "#800080", "#00ffd9", "#808080"]
        i = j = 0
        for color in colors:
            Button(self.color_fill, bg=color, bd=2, relief=RIDGE, width=3, command=lambda col=color: self.select_color(col)).grid(row=i, column=j)
            i = i + 1
            if i == 6:
                i = 0
                j = 1
        # CREATING BUTTONS:
        self.eraser_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/eraser.png").resize((28, 20), Image.ANTIALIAS))
        self.eraser_btn = Button(root, image=self.eraser_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.eraser)
        self.eraser_btn.place(x=0, y=167)
        self.pencil_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/pencil.png.").resize((24, 20), Image.ANTIALIAS))
        self.pencil_btn = Button(root, image=self.pencil_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.pencil)
        self.pencil_btn.place(x=37, y=485)
        self.line_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/line.png").resize((24, 20), Image.ANTIALIAS))
        self.line_but = Button(root, image=self.line_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_line)
        self.line_but.place(x=0, y=485)
        self.colorbox_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/bucket.png").resize((25, 20), Image.ANTIALIAS))
        self.colorbox_btn = Button(root, image=self.colorbox_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=None)
        self.colorbox_btn.place(x=37, y=167)
        self.clear = Button(root, text="Clear", bd=4, bg="white", fg="blue", width=8, relief=RIDGE, command=lambda: self.canvas.delete("all"))
        self.clear.place(x=0, y=197)
        self.canvas = Button(root, text="Canvas", bd=4, bg="white", fg="blue", width=8, relief=RIDGE, command=self.canvas_bg)
        self.canvas.place(x=0, y=227)

        # CREATING SIZE FOR PENCIL AND ERASER
        self.pen_size = LabelFrame(root, bd=5, bg="white", relief=RIDGE)
        self.pen_size.place(x=0, y=260, height=130, width=70)
        self.pen_size1 = Scale(self.pen_size, orient=VERTICAL, from_=50, to=0, length=120)
        self.pen_size1.set(1)
        self.pen_size1.grid(row=0, column=1, padx=15)
        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=900, width=930)
        self.canvas.place(x=80, y=0)
        self.xsb = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))
        self.xsb.pack(side=BOTTOM, fill=X)
        self.ysb.pack(side=RIGHT, fill=Y)
        self.rectangle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Shapes/rectangle.png").resize((24, 20), Image.ANTIALIAS))
        self.rec = Button(root, image=self.rectangle_img, fg="red", bg="white",
                          font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_rectangle)
        self.rec.place(x=0, y=395)
        self.circle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Shapes/circle.png").resize((24, 20), Image.ANTIALIAS))
        self.circle_btn = Button(root, image=self.circle_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_oval)
        self.circle_btn.place(x=0, y=425)
        self.triangle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Shapes/triangle.png").resize((24, 20), Image.ANTIALIAS))
        self.triangle_btn = Button(root, image=self.triangle_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_triangle)
        self.triangle_btn.place(x=37, y=395)
        self.pentagon_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Shapes/pentagon.png").resize((24, 20), Image.ANTIALIAS))
        self.pentagon_btn = Button(root, image=self.pentagon_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_pentagon)
        self.pentagon_btn.place(x=37, y=425)
        self.hexagon_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Shapes/hexagon.png").resize((24, 20), Image.ANTIALIAS))
        self.hexagon_btn = Button(root, image=self.hexagon_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_hexagon)
        self.hexagon_btn.place(x=0, y=455)
        self.parallelogram_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Shapes/parallelogram.png").resize((24, 20), Image.ANTIALIAS))
        self.parallelogram_btn = Button(root, image=self.parallelogram_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.draw_parallelogram)
        self.parallelogram_btn.place(x=37, y=455)
        self.selection_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/selection_box.png").resize((24, 20), Image.ANTIALIAS))
        self.selection_btn = Button(root, image=self.selection_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.select_region)
        self.selection_btn.place(x=0, y=515)
        self.screen_shot_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/Tools/screen_shot.png").resize((24, 20), Image.ANTIALIAS))
        self.screen_shot_btn = Button(root, image=self.screen_shot_img, fg="red", bg="white", font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=self.screen_shot)
        self.screen_shot_btn.place(x=37, y=515)
        # mouse drag
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Motion>", self.coordinates)

    def paint_app(self, event):
        if self.x_start and self.y_start:
            self.stack.append(self.canvas.create_line(self.x_start, self.y_start, event.x, event.y, width=self.pen_size1.get(), fill=self.pen_color, capstyle=ROUND, smooth=True))

        self.x_start = event.x
        self.y_start = event.y

    def reset(self, _):
        self.x_start = None
        self.y_start = None
        self.stack.append('#')

    def reset_rectangle(self):
        self.rect_x0 = 0
        self.rect_y0 = 0
        self.rect_y1 = 0
        self.rect_x1 = 0
        self.temp = []

    def select_color(self, col):
        self.pen_color = col

    def eraser(self):
        self.canvas.config(cursor="dotbox")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.pen_color = "white"

    def coordinates(self, event):
        self.status_bar['text'] = f'{event.x},{event.y}px'

    def canvas_bg(self):
        color = colorchooser.askcolor()
        self.canvas.configure(background=color[1])

    def draw_rectangle(self):
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<ButtonRelease-1>", self.stop_rect)
        self.canvas.bind("<B1-Motion>", self.moving_rect)

    def start_rect(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rect_x0 = self.canvas.canvasx(event.x)
        self.rect_y0 = self.canvas.canvasy(event.y)
        # Create rectangle
        self.rect_id = self.canvas.create_rectangle(
            self.rect_x0, self.rect_y0, self.rect_x0, self.rect_y0, outline=self.pen_color, width=self.pen_size1.get())

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
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_oval)
        self.canvas.bind("<ButtonRelease-1>", self.stop_oval)
        self.canvas.bind("<B1-Motion>", self.moving_oval)

    def start_oval(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.oval_x0 = self.canvas.canvasx(event.x)
        self.oval_y0 = self.canvas.canvasy(event.y)
        # Create oval
        self.oval_id = self.canvas.create_oval(
            self.oval_x0, self.oval_y0, self.oval_x0, self.oval_y0, outline=self.pen_color, width=self.pen_size1.get())

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

    def draw_line(self):
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_line)
        self.canvas.bind("<B1-Motion>", self.moving_line)

    def start_line(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.line_x0 = self.canvas.canvasx(event.x)
        self.line_y0 = self.canvas.canvasy(event.y)
        # Create rectangle
        self.line_id = self.canvas.create_line(
            self.line_x0, self.line_y0, self.line_x0, self.line_y0, fill=self.pen_color, width=self.pen_size1.get(), smooth=True, capstyle=ROUND)

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

    def draw_triangle(self):
        self.triangle_id = None
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_triangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_triangle)
        self.canvas.bind("<B1-Motion>", self.moving_triangle)

    def start_triangle(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.tri_x0 = self.canvas.canvasx(event.x)
        self.tri_y0 = self.canvas.canvasy(event.y)
        # Create triangle
        self.triangle_id = self.canvas.create_polygon(self.tri_x0, self.tri_y0, self.tri_x0 - (event.x - self.tri_x0), event.y, event.x, event.y, outline=self.pen_color, width=self.pen_size1.get(),
                                                      fill='white')

    def moving_triangle(self, event):
        # Modify triangle x1, y1 coordinates
        self.canvas.coords(self.triangle_id, self.tri_x0, self.tri_y0, self.tri_x0 - (event.x - self.tri_x0), event.y, event.x, event.y)

    def stop_triangle(self, event):
        # Modify triangle x1, y1 coordinates
        self.canvas.coords(self.triangle_id, self.tri_x0, self.tri_y0, self.tri_x0 - (event.x - self.tri_x0), event.y, event.x, event.y)
        self.stack.append(self.triangle_id)
        self.stack.append('$')

    def draw_pentagon(self):
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.stop_pentagon)
        self.canvas.bind("<B1-Motion>", self.moving_pentagon)

    def start_pentagon(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.pent_x0 = self.canvas.canvasx(event.x)
        self.pent_y0 = self.canvas.canvasy(event.y)
        # Create pentagon
        self.pentagon_id = self.canvas.create_polygon(self.pent_x0, self.pent_y0, int(self.pent_x0), event.y, event.x, event.y, int(event.x), self.pent_y0,
                                                      (self.pent_x0 + event.x) / 2, self.pent_y0 - 20, outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_pentagon(self, event):
        # Modify pentagon x1, y1 coordinates
        self.canvas.coords(self.pentagon_id, self.pent_x0, self.pent_y0, int(self.pent_x0), event.y, event.x, event.y, int(event.x), self.pent_y0, (self.pent_x0 + event.x) / 2, self.pent_y0 - 20)

    def stop_pentagon(self, event):
        self.canvas.coords(self.pentagon_id, self.pent_x0, self.pent_y0, int(self.pent_x0), event.y, event.x, event.y, int(event.x), self.pent_y0, (self.pent_x0 + event.x) / 2, self.pent_y0 - 20)
        self.stack.append(self.pentagon_id)
        self.stack.append('$')

    def draw_hexagon(self):
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_hexagon)
        self.canvas.bind("<ButtonRelease-1>", self.stop_hexagon)
        self.canvas.bind("<B1-Motion>", self.moving_hexagon)

    def start_hexagon(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.hex_x0 = self.canvas.canvasx(event.x)
        self.hex_y0 = self.canvas.canvasy(event.y)
        # Create hexagon
        self.hexagon_id = self.canvas.create_polygon(self.hex_x0, self.hex_y0, int(self.hex_x0), event.y, (int(self.hex_x0) + int(event.x)) / 2, int(event.y) + 50, event.x, event.y, int(event.x),
                                                     self.hex_y0, (self.hex_x0 + event.x) / 2, self.hex_y0 - 50, outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_hexagon(self, event):
        # Modify hexagon  x1, y1 coordinates
        self.canvas.coords(self.hexagon_id, self.hex_x0, self.hex_y0, int(self.hex_x0), event.y, (int(self.hex_x0) + int(event.x)) / 2, int(event.y) + 50, event.x, event.y, int(event.x), self.hex_y0,
                           (self.hex_x0 + event.x) / 2, self.hex_y0 - 50)

    def stop_hexagon(self, event):
        self.canvas.coords(self.hexagon_id, self.hex_x0, self.hex_y0, int(self.hex_x0), event.y, (int(self.hex_x0) + int(event.x)) / 2, int(event.y) + 50, event.x, event.y, int(event.x), self.hex_y0,
                           (self.hex_x0 + event.x) / 2, self.hex_y0 - 50)
        self.stack.append(self.hexagon_id)
        self.stack.append('$')

    def draw_parallelogram(self):
        self.canvas.config(cursor="fleur")
        self.canvas.bind("<Button-1>", self.start_parallelogram)
        self.canvas.bind("<ButtonRelease-1>", self.stop_parallelogram)
        self.canvas.bind("<B1-Motion>", self.moving_parallelogram)

    def start_parallelogram(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.parallelogram_x0 = self.canvas.canvasx(event.x)
        self.parallelogram_y0 = self.canvas.canvasy(event.y)
        # Create parallelogram
        self.parallelogram_id = self.canvas.create_polygon(self.parallelogram_x0, self.parallelogram_y0, int(self.parallelogram_x0) + 30, event.y, event.x, event.y, int(event.x) - 30,
                                                           self.parallelogram_y0, outline=self.pen_color, width=self.pen_size1.get(), fill='white')

    def moving_parallelogram(self, event):
        # Modify parallelogram x1, y1 coordinates
        self.canvas.coords(self.parallelogram_id, self.parallelogram_x0, self.parallelogram_y0, int(self.parallelogram_x0) + 30, event.y, event.x, event.y, int(event.x) - 30, self.parallelogram_y0)

    def stop_parallelogram(self, event):
        # Modify parallelogram x1, y1 coordinates
        self.canvas.coords(self.parallelogram_id, self.parallelogram_x0, self.parallelogram_y0, int(self.parallelogram_x0) + 30, event.y, event.x, event.y, int(event.x) - 30, self.parallelogram_y0)
        self.stack.append(self.parallelogram_id)
        self.stack.append('$')

    def pencil(self):
        self.canvas.config(cursor="tcross")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.paint_app)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def add_text(self):
        self.top = tk.Toplevel()
        self.top.geometry('310x70')
        text_label = Label(self.top, text="Enter the text", font=("Times", 10, "bold"))
        text_label.grid(row=0, column=0)
        self.entry = Entry(self.top, width=50, relief=SUNKEN, font=("Times", 10, "bold"))
        self.entry.grid(row=1, column=0)
        enter_but = Button(self.top, text="OK", command=self.insert)
        enter_but.grid(row=2, column=0)

    def insert(self):
        self.txt = self.entry.get()
        if len(self.txt) > 0:
            self.top.destroy()
            messagebox.showinfo('Add text',
                                ''' 📣 Please set the mouse pointer from where you want to start the text left click on the mouse to insert then right click to cancel 📣''')

            self.canvas.bind('<Button-1>', self.insert_txt)
            self.canvas.bind('<Button-3>', self.cancel)

    def insert_txt(self, event):
        take = self.canvas.create_text(event.x, event.y, text=self.txt, font=("Times", 10, "bold"))
        self.stack.append(take)
        self.stack.append('$')

    def cancel(self, _):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')

    def zoom_control(self, event):  # For Zoom in and Zoom out
        try:
            if event.delta > 0:
                self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
            elif event.delta < 0:
                self.scale("all", event.x, event.y, 0.9, 0.9)
        except BaseException:
            if event == 1:
                self.canvas.scale("all", 550, 350, 1.1, 1.1)
            else:
                self.canvas.scale("all", 550, 350, 0.9, 0.9)

    def about(self):
        self.top = tk.Toplevel()
        self.top.title("ABOUT")
        self.top.geometry("1350x750")
        self.top.config(bg="pink")
        self.img_label_all = []
        self.des_label_all = []
        self.about_img.clear()
        for i in range(4):
            self.about_img.append(i)
            self.img_label_all.append(i)
            self.des_label_all.append(i)
        self.about_img[0] = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/Menu_bar/colours.png").resize((140, 160), Image.ANTIALIAS))
        self.about_img[1] = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/Menu_bar/width_box.png").resize((140, 160), Image.ANTIALIAS))
        self.about_img[2] = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/Menu_bar/tools.png").resize((140, 160), Image.ANTIALIAS))
        self.about_img[3] = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/Menu_bar/menu_bar.jpeg").resize((160, 160), Image.ANTIALIAS))

        self.heading = Label(self.top, text="All about Tools", font=("Arial", 30, "bold", "italic"), fg="black", bg="pink")
        self.heading.place(x=550, y=10)

        self.img_label_all[0] = Label(self.top, image=self.about_img[0], relief=RAISED, bd=3)
        self.img_label_all[0].place(x=20, y=40)
        self.des_label_all[0] = Label(self.top, text="Color palette and eraser", font=("Arial", 30, "bold"), fg="black", bg="pink")
        self.des_label_all[0].place(x=200, y=100)

        self.img_label_all[1] = Label(self.top, image=self.about_img[1], relief=RAISED, bd=3)
        self.img_label_all[1].place(x=1130, y=170)
        self.des_label_all[1] = Label(self.top, text="Changes the size of your brush and shapes", font=("Arial", 30, "bold"), fg="black", bg="pink")
        self.des_label_all[1].place(x=220, y=220)

        self.img_label_all[2] = Label(self.top, image=self.about_img[2], relief=RAISED, bd=3)
        self.img_label_all[2].place(x=20, y=290)
        self.des_label_all[2] = Label(self.top, text="This box contains all essential tools and shapes", font=("Arial", 30, "bold"), fg="black", bg="pink")
        self.des_label_all[2].place(x=200, y=340)

        self.img_label_all[3] = Label(self.top, image=self.about_img[3], relief=RAISED, bd=3)
        self.img_label_all[3].place(x=1150, y=390)
        self.des_label_all[3] = Label(self.top, text="Menu bar can be accessed through shortcuts", font=("Arial", 30, "bold"), fg="black", bg="pink")
        self.des_label_all[3].place(x=220, y=440)

    def select_region(self):  # For select a region
        try:
            self.draw_selection()

            if self.rect_id:
                self.rect_id = self.canvas.create_rectangle(self.rect_x0, self.rect_y0, self.rect_x0, self.rect_y0, dash=(4, 2), outline="black")

            def select_region_final(_):
                self.temp.append(self.rect_id)

            self.canvas.bind('<ButtonRelease-1>', select_region_final)
            self.canvas.bind('<Button-3>', self.delete)
        except BaseException:
            print("Select region error")

    def delete(self, _):
        self.canvas.delete(self.rect_id)

    def start_selection(self, event):
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rect_x0 = self.canvas.canvasx(event.x)
        self.rect_y0 = self.canvas.canvasy(event.y)
        # Create rectangle
        if not self.rect_id:
            self.rect_id = self.canvas.create_rectangle(self.rect_x0, self.rect_y0, self.rect_x0, self.rect_y0, dash=(4, 2), outline="black")

    def moving_selection(self, event):
        self.rect_x1 = self.canvas.canvasx(event.x)
        self.rect_y1 = self.canvas.canvasy(event.y)

        x, y = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9 * x:
            self.canvas.xview_scroll(1, 'units')
        elif event.x < 0.1 * x:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9 * y:
            self.canvas.yview_scroll(1, 'units')
        elif event.y < 0.1 * y:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect_id, self.rect_x0, self.rect_y0, self.rect_x1, self.rect_y1)

    def delete_selected_region(self, _):  # For delete selected region
        self.canvas.itemconfig(self.rect_id, fill="white", width=0.00001, outline="white")
        self.reset_rectangle()

    def draw_selection(self):
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<ButtonRelease-1>", self.stop_rect)
        self.canvas.bind("<B1-Motion>", self.moving_selection)
        self.canvas.bind(self.place)
        self.canvas.bind('<Delete>', self.delete_selected_region)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def screen_shot(self):
        try:
            self.canvas.delete(self.temp.pop())
            time.sleep(0.0000001)
            root.update()
            x1 = root.winfo_rootx() + self.canvas.winfo_x()
            y1 = root.winfo_rooty() + self.canvas.winfo_y()
            file = filedialog.asksaveasfilename(initialdir="Screen_shots", title="Screen shot save", filetypes=[("PNG File", "*.png")])
            if file:
                ImageGrab.grab().crop((x1 + self.rect_x0, y1 + self.rect_y0, x1 + self.rect_x1, y1 + self.rect_y1)).save(file + ".png")
            self.reset_rectangle()

        except BaseException:
            messagebox.showerror("Selection Error", "First select a region by clicking the selection tool', then take screen shot")


paint = Paint()
root.mainloop()
