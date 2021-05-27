from Module.gui import Gui
from tkinter import PhotoImage
from tkinter import *

root = Tk()
root.attributes("-fullscreen", False)
root.title("DOODLE")
Icon = PhotoImage(file="Utils/Pictures/icon/doodle.png")
root.iconphoto(True, Icon)

gui = Gui()
root.mainloop()
