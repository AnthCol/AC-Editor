import tkinter as tk
from tkinter import ttk
from chlorophyll import CodeView

from .window_events import WINDOW_EVENTS

VIM_CHARS = [
    "<i>", 
    "<h>", 
    "<j>", 
    "<k>", 
    "<l>", 
    "<g>",
    "<Shift-A>", 
    "<Shift-G>",
    "<Shift-asciicircum>", 
    "<Shift-dollar>"
    "0", 
    "1", 
    "2", 
    "3", 
    "4",
    "5", 
    "6", 
    "7", 
    "8", 
    "9"
]

def make_codeview(notebook, settings):
    frame = ttk.Frame(notebook)
    codeview = CodeView(frame, 
                        insertwidth=10, 
                        color_scheme=settings.colour, 
                        font=(settings.font_type, settings.font_size)) 
    codeview.pack(fill="both", expand=True)
    return (codeview, frame)

def fill_codeview(codeview, file):
    failed = False
    content = file.content
    if file.is_unsaved == False:
        try:
            with open(file.path) as f:
                content = f.read()
        except Exception as e:
            tk.messagebox.showerror("Error", "Invalid file type.")
            failed = True
    if not failed:
        codeview.insert(tk.END, content)

def bind_codeview(codeview):
    for char in VIM_CHARS:
        codeview.bind(char, WINDOW_EVENTS["vim"])
    codeview.bind("<Escape>", WINDOW_EVENTS["esc"])
    codeview.bind("<Return>", WINDOW_EVENTS["ret"])
    codeview.bind("<BackSpace>", WINDOW_EVENTS["back"])
