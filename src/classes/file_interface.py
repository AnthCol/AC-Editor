from tkinter import ttk

class FileInterface():
    def __init__(self, window):
        self.notebook = ttk.Notebook(window)
        # Uses the src/classes/file.py class in this list 
        self.files = []
