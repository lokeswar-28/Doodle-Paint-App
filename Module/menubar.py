import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageGrab
from Module.gui import *


class Menubar:
    file_to_open: PhotoImage

    @staticmethod
    def quit():
        root.quit()

    @staticmethod
    def about():
        messagebox.showinfo('DOODLE', 'Go to the help in the main window')

    def __init__(self):
        self.canvas = Button(root, text="Canvas", bd=4, bg="white", width=8, relief=RIDGE, command=Canvas.canvas_bg)
        self.canvas.place(x=0, y=227)
        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=600, width=1000)
        self.canvas.place(x=80, y=0)

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
                                '''📣 Please set the mouse pointer from where you want to start the text left click 
                                on the mouse to insert then right click to cancel 📣''')

            self.canvas.bind('<Button-1>', self.insert_txt)
            self.canvas.bind('<Button-3>', self.cancel)

    def insert_txt(self, event):
        self.canvas.create_text(event.x, event.y, text=self.txt, font=("Times", 10, "bold"))

    def cancel(self, event):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
