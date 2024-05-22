import tkinter as tk
import os
import pygments.lexers 
from tkinter import ttk, filedialog
from chlorophyll import CodeView
from PIL import Image, ImageTk
from .file_datatypes import SavedFile, UnsavedFile
from .code_container import CodeContainer

class GUIManager:

    def __init__(self, gui, settings, database):
        self.gui = gui
        self.notebook = ttk.Notebook(self.gui)
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
    # Saved files (on the drive) must be manually saved, else they will be loaded from memory
    def update_files(self): 
        for container in self.code_containers:
            if isinstance(container.file, UnsavedFile):
                container.file.content = container.codeview.get("1.0", "end-1c")
            # FIXME 
            # Will have some situation where there is a SavedFile object, that
            # needs to be saved 

            # elif isinstance(container.file, SavedFile):
            #     content = container.file.content = container.codeview.get("1.0", "end-1c")
            #     with open(container.file.path, "w") as f:
            #         f.write(content)

    def end(self): 
        # For file in notebook, update content 
        self.update_files()
        self.database.close([container.file for container in self.code_containers])
        self.gui.destroy()

    def get_filename(self, file):
        if isinstance(file, SavedFile):
            return os.path.basename(file.path)
        if isinstance(file, UnsavedFile):
            return "New " + str(file.rank)

    def make_frame(self, file):
        frame = ttk.Frame(self.notebook)

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

    def new(self):


        return

    def open(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            file = SavedFile(filename, len(self.code_containers) + 1)
            self.notebook.add(self.make_frame(file), text=self.pad(self.get_filename(file)))
            self.notebook.select(self.notebook.index("end") - 1)

    def close(self):
        # If unsaved FIXME
        index = self.notebook.index(self.notebook.select())
        del self.code_containers[index]
        self.notebook.forget(index)

    def save(self):
        index = self.notebook.index(self.notebook.select())
        container = self.code_containers[index]
        if isinstance(container.file, SavedFile):
            with open(container.file.path, "w") as f:
                f.write(container.codeview.get("1.0", "end-1c"))
        elif isinstance(container.file, UnsavedFile):
            # Open filedialog to save the file 
            # Name the file in the filedialog
            # Save it somewhere 
            print("temp")
            # Open Save dialogue for unsaved file. 
            # Should be the same code as new. 

    def save_as(self):
        path = filedialog.asksaveasfilename()
        if path != "":
            index = self.notebook.index(self.notebook.select())
            old_unsaved = self.code_containers[index]
            new_saved = SavedFile(path, old_unsaved.file.rank)
            self.code_containers[index].file = new_saved
            self.notebook.tab(index, text=self.pad(self.get_filename(new_saved)))        
            with open(path, "w") as f:
                f.write(self.code_containers[index].codeview.get("1.0", "end-1c"))
            # create file with OS
            # write data to it. 

    def rename(self):
        return

    # Might not bother implementing these we will see  
    def cut(self):
        return
    
    def copy(self):
        return
    
    def paste(self):
        return
    
    def select_all(self):
        return
    
    def theme(self):
        return
    
    def tab_size(self):
        return
    
    def line_endings(self):
        return

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, self.make_icon(LOGO_LOCATION))
        self.gui.protocol("WM_DELETE_WINDOW", self.end)
 
        menubar = tk.Menu(self.gui)

        self.gui.config(menu=menubar)

        file_map = {
            "New" : self.new, 
            "Open" : self.open,
            "Close" : self.close, 
            "Save" : self.save, 
            "Save as" : self.save_as, 
            "Rename" : self.rename
        }

        edit_map = {
            "Cut" : self.cut, 
            "Copy" : self.copy, 
            "Paste" : self.paste, 
            "Select All" : self.select_all
        }

        settings_map = {
            "Theme" : self.theme,
            "Tab Size" : self.tab_size,
            "Line Endings" : self.line_endings
        }

        file_menu = self.create_submenu(menubar, file_map)
        edit_menu = self.create_submenu(menubar, edit_map)
        settings_menu = self.create_submenu(menubar, settings_map)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.open_files = self.database.load_files()
 
        # If there are no files to open, make a blank one always. 
        if len(self.open_files) == 0:
            self.open_files.append(UnsavedFile("", 1))

        for file in self.open_files:
            filename = self.get_filename(file)
            if isinstance(file, UnsavedFile):
                self.notebook.add(self.make_frame(file), text=self.pad(filename))
            elif isinstance(file, SavedFile) and os.path.isfile(file.path):
                self.notebook.add(self.make_frame(file), text=self.pad(filename))

        self.notebook.pack(fill="both", expand=True)

