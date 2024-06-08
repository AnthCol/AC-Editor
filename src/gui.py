import tkinter as tk
import os
import pygments.lexer
import ttkthemes
import pygments.lexers 
from tkinter import ttk, filedialog
from chlorophyll import CodeView
from .file_datatypes import SavedFile, UnsavedFile
from .code_container import CodeContainer
from .auxiliary import make_icon, pad

# FIXME
# With the amount of references to self here, it may be best to just not do the OOP stuff since this is just 
# turning into one massive class. 
# Future problem though. 

class GUIManager:

    def __init__(self, gui, settings, database):
        self.gui = gui
        self.notebook = ttk.Notebook(self.gui)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_change)
        self.style = ttk.Style(self.gui)
        self.style.theme_use('clam')

        self.vim_entry = tk.Entry(self.gui)
        #self.vim_text = tk.Text(self.gui, height=1)
        self.settings = settings
        self.database = database
        self.code_containers = []

        """
            Set things up in the following way:
            Cursor will stay on the codeview
            as the user types, text will be added ELSEWHERE
            and the display will be updated, rather than them having a 
            thing to insert their text into        
        """

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
        self.set_shortcuts()
        self.gui.mainloop()

    
    # Make windows mac distinction here. Check system type and 
    # Do ctrl vs command
    def set_shortcuts(self):
        self.gui.bind("<Control-s>", self.save)
        self.gui.bind("<Control-Alt-s>", self.save_as)
        self.gui.bind("<Control-q>", self.close)
        self.gui.bind("<Control-o>", self.open)
        self.gui.bind("<Control-n>", self.new)
    

    def tab_change(self, event=None):
        index = self.notebook.index(self.notebook.select())
        file = self.code_containers[index].file

        if isinstance(file, SavedFile):
            full_name = file.path 
        else:
            full_name = file.name

        self.gui.title("ac_editor - " + full_name)
        return


    # For now the intended functionality is the following
    # Unsaved files will be "saved"
    # Saved files (on the drive) must be manually saved, else they will be loaded from memory
    # Future situation where we need to check if a saved file is unsaved and save its content
    def update_files(self): 
        rank_counter = 1
        for container in self.code_containers:
            if isinstance(container.file, UnsavedFile):
                container.file.content = container.codeview.get("1.0", "end-1c")
            container.file.rank = rank_counter
            rank_counter += 1


    def end(self): 
        # For file in notebook, update content 
        self.update_files()
        self.database.close([container.file for container in self.code_containers], self.settings)
        self.gui.destroy()


    def make_frame(self, file):
        frame = ttk.Frame(self.notebook)

        lexer = pygments.lexers.TextLexer; 

        if isinstance(file, SavedFile):
            try: 
                lexer = pygments.lexers.get_lexer_for_filename(os.path.basename(file.path))
            except:
                lexer = pygments.lexers.TextLexer

        codeview = CodeView(frame,
                            insertwidth=20,
                            color_scheme=self.settings.colour,
                            font=(self.settings.font_type, self.settings.font_size), 
                            lexer=lexer)

        # FIXME add more error checking later
        if isinstance(file, SavedFile):
            with open(file.path) as f:
                content = f.read()
            codeview.insert(tk.END, content)     
        else:
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
        values = []
        for c in self.code_containers:
            if isinstance(c.file, UnsavedFile):
                values.append(int(c.file.name.split()[1]))
        values.sort()

        count = 1

        for v in values:
            if v != count:
                break
            count += 1
        
        return str(count)
    
    def determine_rank(self):
        return 1 + len(self.code_containers)

    def new(self, event=None):
        file = UnsavedFile("", len(self.code_containers), "New " + self.unsaved_rank())
        self.notebook.add(self.make_frame(file), text=pad(file.name))
        self.show_latest_page()

    def open(self, event=None):
        path = filedialog.askopenfilename()
        if path != "":
            file = SavedFile(path, self.determine_rank(), os.path.basename(path))
            self.notebook.add(self.make_frame(file), text=pad(file.name))
            self.show_latest_page()

    def remove_file(self, index):
        del self.code_containers[index]
        self.notebook.forget(index)

    # FIXME needs refactor. 
    def close(self, event=None):
        index = self.notebook.index(self.notebook.select())
        file = self.code_containers[index].file

        if isinstance(file, UnsavedFile):
            if file.content != "":
                result = tk.messagebox.askyesnocancel("Save File", "Do you want to save this file?")
                if result == True:  
                    self.save_as()
                elif result == False:
                    self.remove_file(index)
            else:
                self.remove_file(index)
        else:
            self.remove_file(index)

        if len(self.code_containers) == 0:
            self.new()


    def save(self, event=None):
        index = self.notebook.index(self.notebook.select())
        container = self.code_containers[index]
        if isinstance(container.file, SavedFile):
            with open(container.file.path, "w") as f:
                f.write(self.codeview_contents(container.codeview))
        else: # UnsavedFile
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename()
        if path != "":
            index = self.notebook.index(self.notebook.select())
            old_unsaved = self.code_containers[index]
            new_saved = SavedFile(path, old_unsaved.file.rank, os.path.basename(path)) 
            self.code_containers[index].file = new_saved
            self.notebook.tab(index, text=pad(new_saved.name))        
            with open(path, "w") as f:
                f.write(self.codeview_contents(self.code_containers[index].codeview))


    # To Be Implemented - Not urgent. 
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
    
    def font_size(self):
        size = tk.simpledialog.askinteger("Font Size", "Input integer for font size:")
        self.settings.font_size = size

    def initialize_gui(self):
        LOGO_LOCATION = "./images/logo.png"
        TITLE = "ac_editor"

        self.gui.title(TITLE)
        self.gui.wm_iconphoto(False, make_icon(LOGO_LOCATION))
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
            "Font Size" : self.font_size, 
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
            open_files.append(UnsavedFile("", 1, "New " + self.unsaved_rank()))

        for file in open_files:
            if isinstance(file, SavedFile) and os.path.isfile(file.path):
                self.notebook.add(self.make_frame(file), text=pad(file.name))
            else:
                self.notebook.add(self.make_frame(file), text=pad(file.name))

        self.notebook.pack(fill="both", side=tk.TOP, expand=True)
        self.vim_entry.pack()
        #self.vim_text.pack(fill="both", side=tk.BOTTOM, expand=True)
