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
LOGO_LOCATION = ".src/images/logo.png"


# FIXME - Need to save the index for the most recently used file somewhere 
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
    # Anchor West doesn't do anything right now because the 
    # size of the label is the size of the text. 
    vim_label = ttk.Label(window, text=vim_controller.message, anchor="w")
    # vim_label.place(relx=0.0, rely=1.0, anchor="w")


    ############################################
    # Initialize lambda function map for events
    ############################################
    event_map = {
        "new"          : lambda: file_new(file_interface, settings),
        "open"         : lambda: file_open(file_interface, settings),
        "save"         : lambda: file_save(file_interface),
        "save_as"      : lambda: file_save_as(file_interface),
        "close"        : lambda: file_close(file_interface),
        "end"          : lambda: end(window, database, settings, file_interface),
        "cut"          : lambda: cut(), 
        "copy"         : lambda: copy(),
        "paste"        : lambda: paste(), 
        "select_all"   : lambda: select_all(),
        "theme"        : lambda: theme(),
        "font_size"    : lambda: font_size(), 
        "tab_size"     : lambda: tab_size(), 
        "line_endings" : lambda: line_endings(),
        "tab_change"   : lambda event: tab_change(window, file_interface, TITLE), 
        "i"            : lambda event: i_press(vim_controller, vim_label), 
        "h"            : lambda event: h_press(vim_controller),
        "j"            : lambda event: j_press(vim_controller),
        "k"            : lambda event: k_press(vim_controller),
        "l"            : lambda event: l_press(vim_controller),
        "num"          : lambda event: number_press(vim_controller), 
        "esc"          : lambda event: esc_press(vim_controller, vim_label),
        "shift_a"      : lambda event: shift_a_press(vim_controller),
        "shift_hat"    : lambda event: shift_hat_press(vim_controller), 
        "shift_dollar" : lambda event: shift_dollar_press(vim_controller), 
    } 


    ##############################
    # Initialize Non-Vim Bindings
    ##############################
    window.protocol("WM_DELETE_WINDOW", event_map["end"])
    window.bind("<Control-s>", event_map["save"])
    window.bind("<Control-Alt-s>", event_map["save_as"])
    window.bind("<Control-q>", event_map["close"])
    window.bind("<Control-o>", event_map["open"])
    window.bind("<Control-n>", event_map["new"])
    file_interface.notebook.bind("<<NotebookTabChanged>>", event_map["tab_change"])

    ##########################
    # Initialize Vim Bindings
    ##########################
    for i in range(10):
        window.bind(str(i), event_map["num"]) 

    window.bind("<i>", event_map["i"]) 
    window.bind("<h>", event_map["h"]) 
    window.bind("<j>", event_map["j"]) 
    window.bind("<k>", event_map["k"]) 
    window.bind("<l>", event_map["l"]) 
    window.bind("<Escape>", event_map["esc"]) 

    window.bind("<Shift-A>", event_map["shift_a"]) 
    window.bind("<Shift-asciicircum>", event_map["shift_hat"]) 
    window.bind("<Shift-dollar>", event_map["shift_dollar"])


    file_map = {
        "New"     : event_map["new"], 
        "Open"    : event_map["open"],
        "Save"    : event_map["save"], 
        "Save as" : event_map["save_as"]
    }

    edit_map = {
        "Cut"        : event_map["cut"], 
        "Copy"       : event_map["copy"], 
        "Paste"      : event_map["paste"],
        "Select All" : event_map["select_all"]
    }

    settings_map = {
        "Theme"        : event_map["theme"], 
        "Font Size"    : event_map["font_size"], 
        "Tab Size"     : event_map["tab_size"], 
        "Line Endings" : event_map["line_endings"]
    }

    menubar = tk.Menu(window)
    
    file_menu = create_submenu(menubar, file_map)
    edit_menu = create_submenu(menubar, edit_map)
    settings_menu = create_submenu(menubar, settings_map)

    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    menubar.add_cascade(label="Settings", menu=settings_menu)
    menubar.add_cascade(label="Close", command=event_map["close"])

    window.config(menu=menubar)

    #################################
    # Load previous data and display
    #################################
    open_files = database.load_files()
    
    if len(open_files) == 0:
        open_files.append(UnsavedFile("", 1, "New " + unsaved_rank(file_interface.containers)))
    
    for f in open_files: 
        file_interface.notebook.add(make_frame(f, settings, file_interface), text=pad(f.name))

    for c in file_interface.containers:
        c.codeview.configure(state="disabled")


    ###########
    # Pack GUI
    ###########
    file_interface.notebook.pack(fill="both", side=tk.TOP, expand=True)
    vim_label.pack()

    ################
    # Start the GUI
    ################
    window.mainloop()
