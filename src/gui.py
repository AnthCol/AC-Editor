import re
import tkinter as tk

from tkinter import ttk
from chlorophyll import CodeView

from .parser import Parser

TITLE = "ac_editor"

class GUI:
    # Constant list 

    def __init__(self, window, file_interface, vim_controller, settings):
        self.window = window
        self.file_interface = file_interface
        self.vim_controller = vim_controller
        self.settings = settings
        self.parser = Parser()

        self.events = { 
            "new"          : lambda event: self.new(),
            "open"         : lambda event: self.open(),
            "save"         : lambda event: self.save(),
            "save_as"      : lambda event: self.save_as(),
            "close"        : lambda event: self.close(),
            "tab_change"   : lambda event: self.tab_change(),
            # Vim Commands
            "vim"          : lambda event: self.process_command(event),
            "esc"          : lambda event: self.esc_press(),
            "return"       : lambda event: self.return_press(),
            "back"         : lambda event: self.backspace_press()
        }

        self.valid = {
            "[0-9]*h" : lambda event: self.h(),
            "[0-9]*j" : lambda event: self.j(),
            "[0-9]*k" : lambda event: self.k(),
            "[0-9]*l" : lambda event: self.l(),
            "i"       : lambda event: self.i(),      
            "A"       : lambda event: self.A(),      
            "\^"      : lambda event: self.hat(),     
            "\$"      : lambda event: self.dollar(),     
            ":w"      : lambda event: self.w(),     
            ":q"      : lambda event: self.q(save=True),     
            ":wq"     : lambda event: self.wq(),    
            ":q!"     : lambda event: self.q(save=False),    
            "gg"      : lambda event: self.gg(),     
            "G"       : lambda event: self.G()
        }

        self.set_window_bindings()
        self.set_notebook_bindings()

    def set_window_bindings(self):
        window = self.window
        events = self.events
        window.bind("<Control-s>", events["save"])
        window.bind("<Control-Alt-s>", events["save_as"])
        window.bind("<Control-q>", events["close"])
        window.bind("<Control-o>", events["open"])
        window.bind("<Control-n>", events["new"])

    def set_notebook_bindings(self):
        notebook = self.file_interface.notebook
        events = self.events
        notebook.bind("<<NotebookTabChanged>>", events["tab_change"])

    def set_file_bindings(self, codeview):
        events = self.events
        vim_commands = [
            "<i>", "<h>", "<j>", "<k>", "<l>", "<g>",
            "<Shift-A>", 
            "<Shift-G>",
            "<Shift-asciicircum>", 
            "<Shift-dollar>"
            "0", "1", "2", "3", "4",
            "5", "6", "7", "8", "9"
        ]
        for command in vim_commands:
            codeview.bind(command, events["vim"])
        codeview.bind("<Escape>", events["esc"])
        codeview.bind("<Return>", events["return"])
        codeview.bind("<BackSpace>", events["back"])

    def add_file(self, file):
        files = self.file_interface.files
        notebook = self.file_interface.notebook 
        settings = self.settings

        frame = ttk.Frame(notebook)

        # FIXME figure out lexer stuff
        codeview = CodeView(frame, 
                            insertwidth=10,
                            color_scheme=settings.colour,
                            font=(settings.font_type, settings.font_size))

        failed = False
        content = file.content

        if file.is_unsaved == False:
            try:
                with open(file.path) as f:
                    content = f.read()
            except Exception as e:
                tk.messagebox.showerror("Error", "Invalid file type.")
                failed = True

        if failed:
            return

        codeview.insert(tk.END, content)
        codeview.pack(fill="both", expand=True)
        
        self.set_file_bindings(codeview)

        # Transfer the codeview over to the file object 
        # Initialized as None previous to this. 
        file.codeview = codeview 

        # Add file to the internal handler, as well as the 
        # notebook for display. 
        files.append(file)
        notebook.add(frame, text=file.name)

        # Show latest page
        notebook.select(notebook.index("end") - 1)

    def is_valid_command(self, command):
        valid = self.valid
        for regex in valid:
            if re.match(regex, command):
                return (True, regex)
        return (False, None)


    def apply_command(self, regex, event=None):
        valid = self.valid 
        for pattern in valid:
            if regex == pattern:
                valid[pattern](event)
 
    def interpret_buffer(self):
        buffer = self.vim_controller.command_buffer
        values = self.is_valid_command(buffer)
        is_valid, regex = values[0], values[1]
        if is_valid:
            self.apply_command(regex)
            self.vim_controller.reset_buffer()

        # Returning break causes tkinter to ignore the default action of the button. 
        # For example, if the user is in normal mode and they press J, we 
        # don't want a j to appear on the screen, only that they move down one line. 
        return "break" if is_valid else None

    def process_command(self, event=None):
        vim_controller = self.vim_controller
        vim_controller.append_buffer(event.char)
        vim_controller.update_display()
        return self.interpret_buffer() 
    
    def tab_change(self):
        notebook = self.file_interface.notebook
        files = self.file_interface.files
        index = notebook.index(notebook.select())
        file = files[index]
        name = file.name if file.is_unsaved else file.path
        self.window.title(TITLE + " - " + name)

    def current_codeview(self):
        notebook = self.file_interface.notebook
        index = notebook.index(notebook.select())
        return self.file_interface.files[index].codeview

    def new():
        return
    def open():
        return
    def save():
        return
    def save_as():
        return
    def close():
        return

    def parse_movement_val(self):
        buffer = self.vim_controller.command_buffer
        return str(self.parser.parse_movement(buffer))

    def h(self):
        codeview = self.current_codeview()
        val = self.parse_movement_val()
        codeview.mark_set("insert", "insert-" + val + "c")

    def j(self, event=None):
        codeview = self.current_codeview()
        val = self.parse_movement_val()
        codeview.mark_set("insert", "insert +" + val + "l")

    def k(self):
        codeview = self.current_codeview()
        val = self.parse_movement_val()
    
    def l(self):
        codeview = self.current_codeview()
        val = self.parse_movement_val()
    
    def i(self):
        return
    def A(self):
        return    
    def hat(self):
        return    
    def dollar(self):
        return    
    def w(self):
        return    
    def q(self, save):
        return    
    def wq(self):
        return    
    def gg(self):
        return    
    def G(self):
        return    