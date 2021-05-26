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

        self.menu_bar()


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
