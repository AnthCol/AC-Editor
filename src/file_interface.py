from tkinter   import ttk

class FileInterface():
    def __init__(self, window):
        self.notebook = ttk.Notebook(window)
        self.containers = []
