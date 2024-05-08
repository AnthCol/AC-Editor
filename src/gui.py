import tkinter as tk
import pygments.lexers 
from tkinter import ttk
from chlorophyll import CodeView
from PIL import Image, ImageTk
from .file_datatypes import SavedFile, UnsavedFile

class GUIManager:

    def __init__(self, gui, settings, database):
        self.gui = gui
        self.settings = settings
        self.database = database

    def make_icon(self, path):
        with Image.open(path) as image:
            icon = ImageTk.PhotoImage(image)
        return icon

    def create_submenu(self, menubar, labels):
        submenu = tk.Menu(menubar, tearoff="off")
        for label in labels:
            submenu.add_command(label=label)
        return submenu

    def new_file_window(self):
        return 

    def update_settings(self, data):
        if data:
            colour, font_type, font_size = data
            self.settings.colour = colour
            self.settings.font_type = font_type
            self.settings.font_size = font_size
        return

    def start(self):
        self.update_settings(self.database.load_settings()) 
        self.initialize_gui()
        self.gui.mainloop()

    def end(self, file_info): 
        self.database.close(file_info)
        self.gui.destroy()

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"
        DEFAULT_LEXER = pygments.lexers.CLexer()

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, self.make_icon(LOGO_LOCATION))
        self.gui.protocol("WM_DELETE_WINDOW", lambda: self.end([]))
 
        # codeview = CodeView(self.gui, 
        #                     lexer=DEFAULT_LEXER, 
        #                     color_scheme=self.settings.colour, 
        #                     font=(self.settings.font_type, self.settings.font_size))

        # codeview.pack(fill="both", expand=True)     
        
        menubar = tk.Menu(self.gui)

        self.gui.config(menu=menubar)

        file_menu = self.create_submenu(menubar, ["New", "Open", "Save As", "Rename"]) 
        edit_menu = self.create_submenu(menubar, ["Cut", "Copy", "Paste", "Select All"])
        settings_menu = self.create_submenu(menubar, ["Theme", "Tab Size", "Line Endings"])

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        #file_list = self.database.load_files()

        # notebook = ttk.Notebook(self.gui)

        # for file in file_list:
        #     frame = ttk.Frame(notebook)
        #     notebook.add(frame, text="Tab" + file.rank) 
        #     codeview = CodeView(self.)
        #     if isinstance(file, SavedFile):
                        
        #     elif isinstance(file, UnsavedFile):

        notebook = ttk.Notebook(self.gui)
        frame1 = ttk.Frame(notebook)
        text1 = tk.Text(frame1)
        text1.pack()
        frame2 = ttk.Frame(notebook)
        text2 = tk.Text(frame2)
        text2.pack()
        notebook.add(frame1)
        notebook.add(frame2)
        notebook.pack(fill="both", expand=True)

