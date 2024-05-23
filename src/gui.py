import tkinter as tk
import os
import pygments.lexers 
from tkinter import ttk, filedialog
from chlorophyll import CodeView
from PIL import Image, ImageTk
from .file_datatypes import SavedFile, UnsavedFile
from .code_container import CodeContainer


# FIXME
# With the amount of references to self here, it may be best to just not do the OOP stuff since this is just 
# turning into one massive class. 
# Future problem though. 


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
        if string != None:
            return "    " + string + "    "

    def start(self):
        self.update_settings(self.database.load_settings()) 
        self.initialize_gui()
        self.set_shortcuts()
        self.gui.mainloop()


    def set_shortcuts(self):
        self.gui.bind("<Control-s>", self.save)
        self.gui.bind("<Control-Alt-s>", self.save_as)
        self.gui.bind("<Control-q>", self.close)
        self.gui.bind("<Control-o>", self.open)
        self.gui.bind("<Control-n>", self.new)
    

    # For now the intended functionality is the following
    # Unsaved files will be "saved"
    # Saved files (on the drive) must be manually saved, else they will be loaded from memory
    def update_files(self): 
        rank_counter = 1
        for container in self.code_containers:
            if isinstance(container.file, UnsavedFile):
                container.file.content = container.codeview.get("1.0", "end-1c")
            container.file.rank = rank_counter
            rank_counter += 1


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
        self.database.close([container.file for container in self.code_containers], self.settings)
        self.gui.destroy()

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

    def last_page_index(self):
        return self.notebook.index("end") - 1

    def codeview_contents(self, codeview):
        return codeview.get("1.0", "end-1c")

    def show_latest_page(self):
        self.notebook.select(self.last_page_index())

    def unsaved_rank(self):
        return 1 + sum(1 for c in self.code_containers if isinstance(c.file, UnsavedFile))

    def determine_rank(self):
        return 1 + len(self.code_containers)

    def new(self):
        file = UnsavedFile("", len(self.code_containers), "New " + str(self.unsaved_rank()))
        self.notebook.add(self.make_frame(file), text=self.pad(file.name))
        self.show_latest_page()

    def open(self):
        path = filedialog.askopenfilename()
        if path != "":
            file = SavedFile(path, self.determine_rank(), os.path.basename(path))
            self.notebook.add(self.make_frame(file), text=self.pad(file.name))
            self.show_latest_page()

    def close(self):
        # If unsaved future FIXME
        index = self.notebook.index(self.notebook.select())
        del self.code_containers[index]
        self.notebook.forget(index)

        if len(self.code_containers) == 0:
            self.new()


    def save(self, event=None):
        index = self.notebook.index(self.notebook.select())
        container = self.code_containers[index]
        if isinstance(container.file, SavedFile):
            with open(container.file.path, "w") as f:
                f.write(self.codeview_contents(container.codeview))
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
            new_saved = SavedFile(path, old_unsaved.file.rank, os.path.basename(path)) 
            self.code_containers[index].file = new_saved
            self.notebook.tab(index, text=self.pad(new_saved.name))        
            with open(path, "w") as f:
                f.write(self.codeview_contents(self.code_containers[index].codeview))


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
            #"Rename" : self.rename
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
        menubar.add_cascade(label="Close", command=self.close)

        open_files = self.database.load_files()
 
        # If there are no files to open (only happens in the case of fresh DB), make a blank one always. 
        if len(open_files) == 0:
            open_files.append(UnsavedFile("", 1, "New 1"))

        for file in open_files:
            if isinstance(file, UnsavedFile):
                self.notebook.add(self.make_frame(file), text=self.pad(file.name))
            elif isinstance(file, SavedFile) and os.path.isfile(file.path):
                self.notebook.add(self.make_frame(file), text=self.pad(file.name))

        self.notebook.pack(fill="both", expand=True)

