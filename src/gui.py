import tkinter as tk

from tkinter import ttk
from chlorophyll import CodeView

TITLE = "ac_editor"

class GUI:
    # Constant list 

    def __init__(self, window, file_interface, vim_controller):
        self.window = window
        self.file_interface = file_interface
        self.vim_controller = vim_controller

        self.EVENTS = { 
            "new"          : lambda event: 10, #file_new(file_interface, settings),
            "open"         : lambda event: 10, #file_open(file_interface, settings, event),
            "save"         : lambda event: 10, #file_save(file_interface, event),
            "save_as"      : lambda event: 10, #file_save_as(file_interface, window, TITLE),
            "close"        : lambda event: 10, #file_close(file_interface, settings),
            "end"          : lambda: 10, #end(window, database, settings, file_interface),
            "tab_change"   : lambda event: self.tab_change(),
            # Vim Commands
            "vim"          : lambda event: self.handle_command(event), #handle_command(vim_controller, file_interface, vim_map, event),
            "esc"          : lambda event: 10, #esc_press(vim_controller),
            "return"       : lambda event: 10, #return_press(vim_controller, file_interface),
            "back"         : lambda event: 10, #backspace_press(vim_controller)
        }

        self.set_window_bindings()
        self.set_notebook_bindings()


    def set_window_bindings(self):
        window = self.window
        EVENTS = self.EVENTS
        window.bind("<Control-s>", EVENTS["save"])
        window.bind("<Control-Alt-s>", EVENTS["save_as"])
        window.bind("<Control-q>", EVENTS["close"])
        window.bind("<Control-o>", EVENTS["open"])
        window.bind("<Control-n>", EVENTS["new"])

    def set_notebook_bindings(self):
        notebook = self.file_interface.notebook
        EVENTS = self.EVENTS
        notebook.bind("<<NotebookTabChanged>>", EVENTS["tab_change"])

    def set_file_bindings(self, codeview):
        EVENTS = self.EVENTS
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
            codeview.bind(command, EVENTS["vim"])
        codeview.bind("<Escape>", EVENTS["esc"])
        codeview.bind("<Return>", EVENTS["return"])
        codeview.bind("<BackSpace>", EVENTS["back"])

    def add_file(self, file, settings):
        files = self.file_interface.files
        notebook = self.file_interface.notebook 

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

    def handle_command(self, event=None):
        buffer = self.vim_controller.command_buffer
        


        return

    def tab_change(self):
        notebook = self.file_interface.notebook
        files = self.file_interface.files
        index = notebook.index(notebook.select())
        file = files[index]
        name = file.name if file.is_unsaved else file.path
        self.window.title(TITLE + " - " + name)


