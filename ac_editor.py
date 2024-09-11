import os
import sys
import pygments.lexers

import tkinter as tk

from tkinter               import ttk

from src.events            import *
from src.settings          import Settings
from src.database          import Database
from src.auxiliary         import make_icon, pad
from src.gui_helpers       import make_frame
from src.file_helpers      import update_files, unsaved_rank
from src.file_datatypes    import UnsavedFile
from src.file_interface    import FileInterface
from src.vim_controller    import VimController

############
# Constants
############
TITLE = "ac_editor"
THEME = "clam"
LOGO_LOCATION = "src/images/logo.png"


# FIXME - Need to save the index for the most recently used file somewhere 
def end(window, database, settings, file_interface):
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
    vim_label = ttk.Label(window, text=vim_controller.message, anchor="w")

    file_interface.notebook.grid(row=0, column=0, sticky="nsew")
    vim_label.grid(row=1, column=0, sticky="ew")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    ############################################
    # Initialize lambda function map for events
    ############################################
    event_map = {
        # Editor Shorcuts
        "new"          : lambda event: file_new(file_interface, settings),
        "open"         : lambda event: file_open(file_interface, settings, event),
        "save"         : lambda event: file_save(file_interface, event),
        "save_as"      : lambda event: file_save_as(file_interface, window, TITLE),
        "close"        : lambda event: file_close(file_interface, settings),
        "end"          : lambda: end(window, database, settings, file_interface),
        "tab_change"   : lambda event: tab_change(window, file_interface, TITLE), 
        # Vim Commands
        "vim"          : lambda event: interpret_command(vim_controller, vim_label, event),
        "esc"          : lambda event: esc_press(vim_controller, vim_label),
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
    vim_commands = []

    for i in range(10):
        vim_commands.append(str(i))
    vim_commands.append("<i>")
    vim_commands.append("<h>")
    vim_commands.append("<j>")
    vim_commands.append("<k>")
    vim_commands.append("<l>")
    vim_commands.append("<Shift-A>")
    vim_commands.append("<Shift-asciicircum>")
    vim_commands.append("<Shift-dollar>")

    for command in vim_commands:
        window.bind(command, event_map["vim"])

    # It is easier to treat escape specially. 
    window.bind("<Escape>", event_map["esc"]) 


    #################################
    # Load previous data and display
    #################################
    open_files = database.load_files()
    
    if len(open_files) == 0:
        open_files.append(UnsavedFile("", 1, "New " + unsaved_rank(file_interface.containers)))
    
    for f in open_files: 
        frame = make_frame(f, settings, file_interface)
        if frame != None:
            file_interface.notebook.add(make_frame(f, settings, file_interface), text=pad(f.name))

    # for c in file_interface.containers:
    #     c.codeview.configure(state="disabled")


    ################
    # Start the GUI
    ################
    window.mainloop()
