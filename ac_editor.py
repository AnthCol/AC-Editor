import os
import sys
import pygments.lexers

import tkinter as tk

from tkinter               import ttk

from src.events            import *
from src.settings          import Settings
from src.database          import Database
from src.auxiliary         import make_icon, pad
from src.gui_helpers       import create_submenu, make_frame
from src.file_helpers      import update_files, unsaved_rank
from src.file_datatypes    import UnsavedFile
from src.file_interface    import FileInterface
from src.vim_controller    import VimController

############
# Constants
############
TITLE = "ac_editor"
THEME = "clam"
LOGO_LOCATION = "./images/logo.png"


def end(window, database, settings, file_interface, event=None):
    update_files(file_interface.containers)
    database.close([c.file for c in file_interface.containers], settings)
    window.destroy()


if __name__ == "__main__":
    #################
    # Necessary Data
    #################
    window = tk.Tk()
    settings = Settings()
    database = Database()
    vim_controller = VimController()
    file_interface = FileInterface(window)

    ##############################
    # Initialize Non-Vim Bindings
    ##############################
    window.protocol("WM_DELETE_WINDOW", lambda: end(window, database, settings, file_interface))
    window.bind("<Control-s>",          lambda: file_save(file_interface))
    window.bind("<Control-Alt-s>",      lambda: file_save_as(file_interface))
    window.bind("<Control-q>",          lambda: file_close(file_interface))
    window.bind("<Control-o>",          lambda: file_open(file_interface, settings))
    window.bind("<Control-n>",          lambda: file_new(file_interface))
    file_interface.notebook.bind("<<NotebookTabChanged>>", lambda event : tab_change(window, file_interface, event))

    ##########################
    # Initialize Vim Bindings
    ##########################
    for i in range(10):
        window.bind(str(i), lambda: number_press(vim_controller))

    window.bind("<i>", lambda event: i_press(vim_controller))
    window.bind("<h>", lambda event: h_press(vim_controller))
    window.bind("<j>", lambda event: j_press(vim_controller))
    window.bind("<k>", lambda event: k_press(vim_controller))
    window.bind("<l>", lambda event: l_press(vim_controller))

    window.bind("<Shift-A>",           lambda event: shift_a_press(vim_controller))
    window.bind("<Shift-asciicircum>", lambda event: shift_hat_press(vim_controller))
    window.bind("<Shift-dollar>",      lambda event: shift_dollar_press(vim_controller))

    
    ################
    # Load settings
    ################
    data = database.load_settings()
    if data:
        colour, font_type, font_size = data
        settings.colour    = colour
        settings.font_type = font_type
        settings.font_size = font_size

    #######################
    # Initialize aesthetic
    #######################
    window.title(TITLE)
    window.wm_iconphoto(False, make_icon(LOGO_LOCATION))
    _ = ttk.Style(window).theme_use(THEME)


    file_map = {
        "New"     : lambda: file_new(file_interface, settings),
        "Open"    : lambda: file_open(file_interface, settings),
        "Save"    : lambda: file_save(file_interface),
        "Save as" : lambda: file_save_as(file_interface), 
    }

    edit_map = {
        "Cut"        : lambda: cut(), 
        "Copy"       : lambda: copy(), 
        "Paste"      : lambda: paste(), 
        "Select All" : lambda: select_all(),
    }

    settings_map = {
        "Theme"        : lambda: theme(),
        "Font Size"    : lambda: font_size(), 
        "Tab Size"     : lambda: tab_size(),
        "Line Endings" : lambda: line_endings(),
    }

    menubar = tk.Menu(window)
    
    file_menu = create_submenu(menubar, file_map)
    edit_menu = create_submenu(menubar, edit_map)
    settings_menu = create_submenu(menubar, settings_map)

    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    menubar.add_cascade(label="Settings", menu=settings_menu)
    menubar.add_cascade(label="Close", command=lambda: file_close(file_interface, settings))

    window.config(menu=menubar)

    #####################
    # Load previous data
    #####################
    open_files = database.load_files()
    
    if len(open_files) == 0:
        open_files.append(UnsavedFile("", 1, "New " + unsaved_rank(file_interface.containers)))
    
    for f in open_files: 
        file_interface.notebook.add(make_frame(f, settings, file_interface), text=pad(f.name))

    file_interface.notebook.pack(fill="both", side=tk.TOP, expand=True)

    ################
    # Start the GUI
    ################
    window.mainloop()
