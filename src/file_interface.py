from tkinter   import ttk
from dataclasses import dataclass 

@dataclass
class FileInterface():
    def __init__(self, window):
        self.notebook = ttk.Notebook(window)
        self.containers = []
