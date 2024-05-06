import tkinter as tk
import pygments.lexers 
from chlorophyll import CodeView
from PIL import Image, ImageTk
from settings import Settings

def make_icon(path):
    icon = Image.open(path)
    return ImageTk.PhotoImage(icon)

def initialize_gui(settings):
    gui = tk.Tk()
    gui.title("ac_editor")

    gui.wm_iconphoto(False, make_icon("./resources/logo.png"))

    codeview = CodeView(gui, 
                        lexer=pygments.lexers.CLexer(), 
                        color_scheme=settings.colour, 
                        font=(settings.font_type, settings.font_size))

    codeview.pack(fill="both", expand=True)     
    
    menubar = tk.Menu(gui)

    gui.config(menu=menubar)

    file_menu = tk.Menu(menubar)
    edit_menu = tk.Menu(menubar)
    settings_menu = tk.Menu(menubar)

    file_menu.add_command(label = "New")
    file_menu.add_command(label = "Open")
    file_menu.add_command(label = "Save As")
    file_menu.add_command(label = "Rename")

    edit_menu.add_command(label = "Cut")
    edit_menu.add_command(label = "Copy")
    edit_menu.add_command(label = "Paste")
    edit_menu.add_command(label = "Select All")

    settings_menu.add_command(label = "Theme")
    settings_menu.add_command(label = "Tab Size")
    settings_menu.add_command(label = "Line Endings")

    menubar.add_cascade(label = "File", menu=file_menu)
    menubar.add_cascade(label = "Edit", menu=edit_menu)
    menubar.add_cascade(label = "Settings", menu=settings_menu)

    return gui



if (__name__ == "__main__"):
    settings = Settings()
    settings.load()
    window = initialize_gui(settings)
    window.mainloop()
    settings.save()
    
