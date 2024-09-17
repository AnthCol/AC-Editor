from typing import List
from tkinter import ttk

from .file import File

class FileInterface():
    def __init__(self, window):
        self.notebook = ttk.Notebook(window)
        self.files = List[File] = []
