from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter.ttk import Scale
from PIL import ImageTk, Image, ImageGrab
from tkinter import colorchooser

root = Tk()
root.attributes("-fullscreen", False)
root.title("DOODLE")
Icon = PhotoImage(file="Utils/Pictures/icon/doodle.png")
root.iconphoto(True, Icon)


class Paint:
    # Initialisation
    x_start, y_start = 0, 0
    line_x0, line_y0, line_x1, line_y1 = 0, 0, 0, 0
    file_to_open: PhotoImage

    @staticmethod
    def quit():
        root.quit()

    @staticmethod
    def about():
        messagebox.showinfo('DOODLE', 'Go to the help in the main window')

    def open_file(self):
        try:
            filename = filedialog.askopenfilename(initialdir="/", filetypes=(
                ("jpeg files", "*.jpg"), ("png files", "*.png")))
            image = Image.open(filename)
            image.save("Temp.png", "png")
            self.file_to_open = PhotoImage(file="Temp.png")
            self.canvas.delete("all")
            self.canvas.create_image(3, 3, image=self.file_to_open, anchor=NW)
        except AttributeError:
            pass

    def save_file(self):
        file = filedialog.asksaveasfilename(initialdir="/", filetypes=(
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

        # EDIT MENU
        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menu.add_cascade(label="✒ Edit", menu=edit_menu)

        # TEXT MENU
        text_menu = Menu(menu, tearoff=0)
        text_menu.add_command(label="Text", command=self.add_text)
        menu.add_cascade(label="🖊 Text", menu=text_menu)

        # HELP MENU
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="⁉ About", command=self.about)
        menu.add_cascade(label="❓ Help", menu=help_menu)

        root.config(menu=menu)
        root.bind("<Control-z>", self.undo)

    def __init__(self):
        self.stack = []
        self.item = None
        self.status_bar = Label(bd=5, relief=RIDGE, font='Times 15 bold', bg='white', fg='black', anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
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
        self.menu_bar()
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
        self.clear = Button(root, text="Clear", bd=4, bg="white", width=8, relief=RIDGE,
                            command=lambda: self.canvas.delete("all"))
        self.clear.place(x=0, y=197)
        self.canvas = Button(root, text="Canvas", bd=4, bg="white", width=8, relief=RIDGE, command=self.canvas_bg)
        self.canvas.place(x=0, y=227)

        # CREATING SIZE FOR PENCIL AND ERASER
        self.pen_size = LabelFrame(root, bd=5, bg="white", relief=RIDGE)
        self.pen_size.place(x=0, y=260, height=130, width=70)
        self.pen_size1 = Scale(self.pen_size, orient=VERTICAL, from_=50, to=0, length=120)
        self.pen_size1.set(1)
        self.pen_size1.grid(row=0, column=1, padx=15)
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

    def select_color(self, col):
        self.pen_color = col

    def eraser(self):
        self.pen_color = "white"

    def coordinates(self, event):
        self.status_bar['text'] = f'{event.x},{event.y}px'

    def canvas_bg(self):
        color = colorchooser.askcolor()
        self.canvas.configure(background=color[1])



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

    def add_text(self):
        global top, entry
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
        self.canvas.create_text(event.x, event.y, text=self.txt, font=("Times", 10, "bold"))

    def cancel(self, event):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')

    def zoom_control(self, event):  # For Zoom in and Zoom out
        try:
            if event.delta > 0:
                self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
            elif event.delta < 0:
                self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        except:
            if event == 1:
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


paint = Paint()
root.mainloop()
