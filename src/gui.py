import tkinter as tk

EVENTS = {


}

class GUI:
    def __init__(self, window, file_interface, vim_controller):
        self.window = window
        self.file_interface = file_interface
        self.vim_controller = vim_controller

        self.set_window_bindins()
        self.set_notebook_bindings()

    def set_window_bindings(self):
        window = self.window
        window.protocol("WM_DELETE_WINDOW", event_map["end"])
        window.bind("<Control-s>", event_map["save"])
        window.bind("<Control-Alt-s>", event_map["save_as"])
        window.bind("<Control-q>", event_map["close"])
        window.bind("<Control-o>", event_map["open"])
        window.bind("<Control-n>", event_map["new"])

    def set_notebook_bindings(self):
        notebook = self.file_interface.notebook
        notebook.bind("<<NotebookTabChanged>>", event_map["tab_change"])

    def set_file_bindings():
        return

    def add_file(self, file, settings):
        notebook = self.file_interface.notebook 
        notebook.add
        return