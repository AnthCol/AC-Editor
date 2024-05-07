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

    def close_window(self):
        # FIXME need to add saving for files here 
        self.database.rewrite(self.settings)
        self.gui.destroy()

    def create_submenu(menubar, labels):
        submenu = tk.Menu(menubar, tearoff="off")
        for label in labels:
            submenu.add_command(label=label)
        return submenu

    def new_file_window():
        return 

    def run(self):
        self.gui.mainloop()

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"
        DEFAULT_LEXER = pygments.lexers.CLexer()

        self.settings.load()

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, self.make_icon(LOGO_LOCATION))
        self.gui.protocol("WM_DELETE_WINDOW", lambda: self.close_window(self.gui, self.settings))


        # codeview = CodeView(gui, 
        #                     lexer=DEFAULT_LEXER, 
        #                     color_scheme=settings.colour, 
        #                     font=(settings.font_type, settings.font_size))

        # codeview.pack(fill="both", expand=True)     
        
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

        codeview1 = CodeView(self.gui, 
                            lexer=DEFAULT_LEXER, 
                            color_scheme=self.settings.colour, 
                            font=(self.settings.font_type, self.settings.font_size))

        codeview1.pack(fill="both", expand=True)     

        # codeview2 = CodeView(gui, 
        #                     lexer=DEFAULT_LEXER, 
        #                     color_scheme=settings.colour, 
        #                     font=(settings.font_type, settings.font_size))

        # codeview2.pack(fill="both", expand=True)     

        # notebook.add(codeview1)
        # notebook.add(codeview2)

        return gui