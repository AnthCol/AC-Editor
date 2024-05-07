import tkinter as tk
import pygments.lexers 
from tkinter import ttk
from chlorophyll import CodeView
from PIL import Image, ImageTk
from settings import Settings
from database import Database


class GUIManager:

    def __init__(self, gui, settings, database):
        self.gui = gui
        self.settings = settings
        self.database = database

    def make_icon(path):
        with Image.open(path) as image:
            icon = ImageTk.PhotoImage(image)
        return icon

    def create_submenu(menubar, labels):
        submenu = tk.Menu(menubar, tearoff="off")
        for label in labels:
            submenu.add_command(label=label)
        return submenu

    def new_file_window():
        return 

    def start(self):
        self.database.load_settings(self.settings)
        self.initialize_gui()
        self.gui.mainloop()

    def end(self, file_info):
        self.database.rewrite(self.settings, file_info)
        self.database.close()
        self.gui.destroy()

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"
        DEFAULT_LEXER = pygments.lexers.CLexer()

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, self.make_icon(LOGO_LOCATION))
        self.gui.protocol("WM_DELETE_WINDOW", self.end)

        codeview = CodeView(self.gui, 
                            lexer=DEFAULT_LEXER, 
                            color_scheme=self.settings.colour, 
                            font=(self.settings.font_type, self.settings.font_size))

        codeview.pack(fill="both", expand=True)     
        
        menubar = tk.Menu(self.gui)

        self.gui.config(menu=menubar)

        file_menu = self.create_submenu(menubar, ["New", "Open", "Save As", "Rename"]) 
        edit_menu = self.create_submenu(menubar, ["Cut", "Copy", "Paste", "Select All"])
        settings_menu = self.create_submenu(menubar, ["Theme", "Tab Size", "Line Endings"])

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # notebook = ttk.Notebook(gui)
        # notebook.pack(expand=1, fill="both")

        # codeview1 = CodeView(self.gui, 
        #                     lexer=DEFAULT_LEXER, 
        #                     color_scheme=self.settings.colour, 
        #                     font=(self.settings.font_type, self.settings.font_size))

        # codeview1.pack(fill="both", expand=True)     

        # codeview2 = CodeView(gui, 
        #                     lexer=DEFAULT_LEXER, 
        #                     color_scheme=settings.colour, 
        #                     font=(settings.font_type, settings.font_size))

        # codeview2.pack(fill="both", expand=True)     

        # notebook.add(codeview1)
        # notebook.add(codeview2)
        return