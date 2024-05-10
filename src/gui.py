import tkinter as tk
import os
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
        self.open_files = []

    def make_icon(self, path):
        with Image.open(path) as image:
            icon = ImageTk.PhotoImage(image)
        return icon

    def create_submenu(self, menubar, labels):
        submenu = tk.Menu(menubar, tearoff="off")
        for label in labels:
            submenu.add_command(label=label)
        return submenu

    def update_settings(self, data):
        if data:
            colour, font_type, font_size = data
            self.settings.colour = colour
            self.settings.font_type = font_type
            self.settings.font_size = font_size
        return

    def pad(self, string):
        return "    " + string + "    "

    def start(self):
        self.update_settings(self.database.load_settings()) 
        self.initialize_gui()
        self.gui.mainloop()

    def end(self): 
        self.database.close(self.open_files)
        self.gui.destroy()

    def get_filename(self, file):
        if isinstance(file, SavedFile):
            return os.path.basename(file.path)
        elif isinstance(file, UnsavedFile):
            return "New " + str(file.rank)

    def make_frame(self, notebook, file):
        frame = ttk.Frame(notebook)

        codeview = CodeView(frame,
                            color_scheme=self.settings.colour,
                            font=(self.settings.font_type, self.settings.font_size))

        if isinstance(file, SavedFile):
            with open(file.path) as f:
                content = f.read()
            codeview.insert(tk.END, content)     
        elif isinstance(file, UnsavedFile): 
            codeview.insert(tk.END, file.content)

        codeview.pack(fill="both", expand=True)
        return frame

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, self.make_icon(LOGO_LOCATION))
        self.gui.protocol("WM_DELETE_WINDOW", self.end)
 
        menubar = tk.Menu(self.gui)

        self.gui.config(menu=menubar)

        file_menu = self.create_submenu(menubar, ["New", "Open", "Save As", "Rename"]) 
        edit_menu = self.create_submenu(menubar, ["Cut", "Copy", "Paste", "Select All"])
        settings_menu = self.create_submenu(menubar, ["Theme", "Tab Size", "Line Endings"])

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        notebook = ttk.Notebook(self.gui)

        self.open_files = self.database.load_files()

        # If there are no files to open, make a blank one always. 
        if len(self.open_files) == 0:
            self.open_files.append(UnsavedFile("", 1))

        for file in self.open_files:
            filename = self.get_filename(file)
            notebook.add(self.make_frame(notebook, file), text=self.pad(filename))

        notebook.pack(fill="both", expand=True)
