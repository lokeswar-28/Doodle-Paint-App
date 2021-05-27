from tkinter import *
from Module.canvas import Canvas
from Module.menubar import Menubar
from PIL import ImageTk, Image
from Module.tools import Tools
from doodle import root
from Module.shapes import Shapes


class Gui:

    def menu_bar(self):
        menu = Menu(root)
        # FILE MENU
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="📂 Open", command=Menubar.open_file)
        file_menu.add_command(label="📥 Save", command=Menubar.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Quit", command=Menubar.quit)
        menu.add_cascade(label="🗂 File", menu=file_menu)

        # EDIT MENU
        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=Tools.undo, accelerator="Ctrl+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menu.add_cascade(label="✒ Edit", menu=edit_menu)

        # TEXT MENU
        text_menu = Menu(menu, tearoff=0)
        text_menu.add_command(label="Text", command=Menubar.add_text)
        menu.add_cascade(label="🖊 Text", menu=text_menu)

        # HELP MENU
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="⁉ About", command=Menubar.about)
        menu.add_cascade(label="❓ Help", menu=help_menu)

        root.config(menu=menu)
        root.bind("<Control-z>", Tools.undo)

    def __init__(self):

        self.clear = Button(root, text="Clear", bd=4, bg="white", width=8, relief=RIDGE,
                            command=lambda: self.canvas.delete("all"))
        self.clear.place(x=0, y=197)

        self.canvas = Button(root, text="Canvas", bd=4, bg="white", width=8, relief=RIDGE, command=Canvas.canvas_bg)
        self.canvas.place(x=0, y=227)

        self.canvas = Canvas(root, bd=6, bg="white", relief=GROOVE, height=600, width=1000)
        self.canvas.place(x=80, y=0)

        self.xsb = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(root, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))

        self.xsb.pack(side=BOTTOM, fill=X)
        self.ysb.pack(side=RIGHT, fill=Y)

        # mouse drag
        self.canvas.bind("<B1-Motion>", Canvas.paint_app)
        self.canvas.bind("<ButtonRelease-1>", Canvas.reset)
        self.canvas.bind("<Motion>", Canvas.coordinates)

        self.rectangle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/shapes/rectangle.png").resize((24, 20),
                                                                                                         Image.ANTIALIAS))
        self.rec = Button(root, image=self.rectangle_img, fg="red", bg="white",
                          font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=Shapes.draw_rectangle)
        self.rec.place(x=0, y=395)

        self.circle_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/shapes/circle.png").resize((24, 20), Image.ANTIALIAS))
        self.circle_btn = Button(root, image=self.circle_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=Shapes.draw_oval)
        self.circle_btn.place(x=0, y=425)

        self.triangle_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/shapes/triangle.png").resize((24, 20),
                                                                                                       Image.ANTIALIAS))
        self.triangle_btn = Button(root, image=self.triangle_img, fg="red", bg="white",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=Shapes.draw_triangle)
        self.triangle_btn.place(x=37, y=395)

        self.pentagon_img = ImageTk.PhotoImage(Image.open("Utils/Pictures/shapes/pentagon.png").resize((24, 20),
                                                                                                       Image.ANTIALIAS))
        self.pentagon_btn = Button(root, image=self.pentagon_img, fg="red", bg="white",
                                   font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=Shapes.draw_pentagon)
        self.pentagon_btn.place(x=37, y=425)
        self.hexagon_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/shapes/hexagon.png").resize((24, 20), Image.ANTIALIAS))
        self.hexagon_btn = Button(root, image=self.hexagon_img, fg="red", bg="white",
                                  font=("Arial", 10, "bold"), relief=RAISED, bd=3, command=Shapes.draw_hexagon)
        self.hexagon_btn.place(x=0, y=455)
        self.parallelogram_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/shapes/parallelogram.png").resize((24, 20), Image.ANTIALIAS))
        self.parallelogram_btn = Button(root, image=self.parallelogram_img, fg="red", bg="white",
                                        font=("Arial", 10, "bold"), relief=RAISED, bd=3,
                                        command=Shapes.draw_parallelogram)
        self.parallelogram_btn.place(x=37, y=455)

        self.zoom_in_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/zoom in.png").resize((25, 20), Image.ANTIALIAS))
        self.zoom_in = Button(image=self.zoom_in_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                              relief=RAISED, bd=3, command=lambda: Tools.zoom_control(1))
        self.zoom_in.place(x=1315, y=600)
        self.zoom_out_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/zoom out.png").resize((25, 20), Image.ANTIALIAS))
        self.zoom_out = Button(image=self.zoom_out_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                               relief=RAISED, bd=3, command=lambda: Tools.zoom_control(0))
        self.zoom_out.place(x=1275, y=600)
        self.pen_color = "black"
        self.color_fill = LabelFrame(root, bd=5, relief=RIDGE, bg="white")
        self.color_fill.place(x=0, y=0, width=70, height=165)
        colors = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFD700", "#FF00FF", "#FFC0CB",
                  "#800080", "#00ffd9", "#808080"]
        i = j = 0
        for color in colors:
            Button(self.color_fill, bg=color, bd=2, relief=RIDGE, width=3,
                   command=lambda col=color: Tools.select_color(col)).grid(row=i, column=j)
            i = i + 1
            if i == 6:
                i = 0
                j = 1
        # CREATING BUTTONS:
        self.eraser_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/eraser.png").resize((28, 20), Image.ANTIALIAS))
        self.eraser_btn = Button(root, image=self.eraser_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=Tools.eraser)
        self.eraser_btn.place(x=0, y=167)
        self.pencil_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/pencil.png.").resize((24, 20), Image.ANTIALIAS))
        self.pencil_btn = Button(root, image=self.pencil_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                                 relief=RAISED, bd=3, command=Tools.pencil)
        self.pencil_btn.place(x=37, y=485)
        self.line_img = ImageTk.PhotoImage(
            Image.open("Utils/Pictures/tools/line.png").resize((24, 20), Image.ANTIALIAS))
        self.line_but = Button(root, image=self.line_img, fg="red", bg="white", font=("Arial", 10, "bold"),
                               relief=RAISED, bd=3, command=Tools.draw_line)
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

        self.stack = []
        self.item = None
        self.status_bar = Label(bd=5, relief=RIDGE, font='Times 15 bold', bg='white', fg='black', anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

        self.menu_bar()


gui = Gui()
root.mainloop()
