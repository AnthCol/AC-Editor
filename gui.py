import tkinter as tk
import pygments.lexers 
from tkinter import ttk
from chlorophyll import CodeView
from PIL import Image, ImageTk
from settings import Settings


def make_icon(path):
    with Image.open(path) as image:
        icon = ImageTk.PhotoImage(image)
    return icon

def close_window(gui, settings):
    settings.save() 
    gui.destroy()

def create_submenu(menubar, labels):
    submenu = tk.Menu(menubar, tearoff="off")
    for label in labels:
        submenu.add_command(label=label)
    return submenu

def new_file_window():
    return 

def initialize_gui(settings):
    LOGO_LOCATION = "./resources/logo.png"
    TITLE = "ac_editor"
    DEFAULT_LEXER = pygments.lexers.CLexer()

    settings.load()

    gui = tk.Tk()
    gui.title(TITLE)
    gui.wm_iconphoto(False, make_icon(LOGO_LOCATION))
    gui.protocol("WM_DELETE_WINDOW", lambda: close_window(gui, settings))


    # codeview = CodeView(gui, 
    #                     lexer=DEFAULT_LEXER, 
    #                     color_scheme=settings.colour, 
    #                     font=(settings.font_type, settings.font_size))

    # codeview.pack(fill="both", expand=True)     
    
    menubar = tk.Menu(gui)

    gui.config(menu=menubar)

    file_menu = create_submenu(menubar, ["New", "Open", "Save As", "Rename"]) 
    edit_menu = create_submenu(menubar, ["Cut", "Copy", "Paste", "Select All"])
    settings_menu = create_submenu(menubar, ["Theme", "Tab Size", "Line Endings"])

    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    menubar.add_cascade(label="Settings", menu=settings_menu)

    # notebook = ttk.Notebook(gui)
    # notebook.pack(expand=1, fill="both")

    codeview1 = CodeView(gui, 
                        lexer=DEFAULT_LEXER, 
                        color_scheme=settings.colour, 
                        font=(settings.font_type, settings.font_size))

    codeview1.pack(fill="both", expand=True)     

    # codeview2 = CodeView(gui, 
    #                     lexer=DEFAULT_LEXER, 
    #                     color_scheme=settings.colour, 
    #                     font=(settings.font_type, settings.font_size))

    # codeview2.pack(fill="both", expand=True)     

    # notebook.add(codeview1)
    # notebook.add(codeview2)

    return gui