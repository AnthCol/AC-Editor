import tkinter as tk
import pygments.lexers 
from chlorophyll import CodeView
from PIL import Image, ImageTk
from settings import Settings

def make_icon(path):
    icon = Image.open(path)
    return ImageTk.PhotoImage(icon)

def close_window(gui, settings):
    settings.save() 
    gui.destroy()

def create_submenu(menubar, labels):
    submenu = tk.Menu(menubar)
    for label in labels:
        submenu.add_command(label=label)
    return submenu

def initialize_gui(settings):
    LOGO_LOCATION = "./resources/logo.png"
    TITLE = "ac_editor"
    DEFAULT_LEXER = pygments.lexers.CLexer()

    settings.load()

    gui = tk.Tk()
    gui.title(TITLE)
    gui.wm_iconphoto(False, make_icon(LOGO_LOCATION))
    gui.protocol("WM_DELETE_WINDOW", lambda: close_window(gui, settings))

    codeview = CodeView(gui, 
                        lexer=DEFAULT_LEXER, 
                        color_scheme=settings.colour, 
                        font=(settings.font_type, settings.font_size))

    codeview.pack(fill="both", expand=True)     
    
    menubar = tk.Menu(gui)

    gui.config(menu=menubar)

    file_menu = create_submenu(menubar, ["New", "Open", "Save As", "Rename"]) 
    edit_menu = create_submenu(menubar, ["Cut", "Copy", "Paste", "Select All"])
    settings_menu = create_submenu(menubar, ["Theme", "Tab Size", "Line Endings"])

    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    menubar.add_cascade(label="Settings", menu=settings_menu)

    return gui


if (__name__ == "__main__"):
    gui = initialize_gui(Settings())
    gui.mainloop()
    
