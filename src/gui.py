import tkinter as tk
import os
import pygments.lexers 
from tkinter import ttk
from chlorophyll import CodeView
from PIL import Image, ImageTk
from .file_datatypes import SavedFile, UnsavedFile
from .code_container import CodeContainer

class GUIManager:

    def __init__(self, gui, settings, database):
        self.gui = gui
        self.settings = settings
        self.database = database
        self.code_containers = []

    def make_icon(self, path):
        with Image.open(path) as image:
            icon = ImageTk.PhotoImage(image)
        return icon


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

    # For now the intended functionality is the following
    # Unsaved files will be "saved"
    # Saved files (on the drivE) must be manually saved, else they will be loaded from memory

    def update_files(self):
        for container in self.code_containers:
            if isinstance(container.file, UnsavedFile):
                container.file.content = container.codeview.get("1.0", "end-1c")

    def end(self): 
        self.update_files()
        self.database.close([container.file for container in self.code_containers])
        self.gui.destroy()

    def get_filename(self, file):
        if isinstance(file, SavedFile):
            return os.path.basename(file.path)
        if isinstance(file, UnsavedFile):
            return "New " + str(file.rank)

    def make_frame(self, notebook, file):
        frame = ttk.Frame(notebook)

        codeview = CodeView(frame,
                            color_scheme=self.settings.colour,
                            font=(self.settings.font_type, self.settings.font_size))

        # FIXME add more error checking later
        if isinstance(file, SavedFile):
            with open(file.path) as f:
                content = f.read()
            codeview.insert(tk.END, content)     
        elif isinstance(file, UnsavedFile): 
            codeview.insert(tk.END, file.content)

        codeview.pack(fill="both", expand=True)

        self.code_containers.append(CodeContainer(file=file, codeview=codeview))

        return frame

    def create_submenu(self, menubar, map):
        submenu = tk.Menu(menubar, tearoff="off")
        for key, value in map.items():
            submenu.add_command(label=key, command=value)
        return submenu

    def func(self):
        print("test")

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, self.make_icon(LOGO_LOCATION))
        self.gui.protocol("WM_DELETE_WINDOW", self.end)
 
        menubar = tk.Menu(self.gui)

        self.gui.config(menu=menubar)

        file_map = {
            "New" : self.func, 
            "Open" : self.func, 
            "Save" : self.func, 
            "Save as" : self.func, 
            "Rename" :self.func
        }

        edit_map = {
            "Cut" : self.func, 
            "Copy" : self.func, 
            "Paste" : self.func, 
            "Select All" : self.func
        }

        settings_map = {
            "Theme" : self.func, 
            "Tab Size" : self.func, 
            "Line Endings" : self.func
        }

        file_menu = self.create_submenu(menubar, file_map)
        edit_menu = self.create_submenu(menubar, edit_map)
        settings_menu = self.create_submenu(menubar, settings_map)

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

