import os
import sys
import pygments.lexers

import tkinter as tk

from tkinter               import ttk

from src.events       import *
from src.auxiliary    import make_icon, pad
# from src.gui_helpers  import make_frame
# from src.file_helpers import update_files, unsaved_rank

from src.gui            import GUI
from src.file           import File
from src.settings       import Settings
from src.database       import Database
from src.vim_controller import VimController
from src.file_interface import FileInterface

###########################################################
# Constants 
# (FIXME, theme should be moved to Settings in the future)
###########################################################
TITLE = "ac_editor"
THEME = "clam"
LOGO_LOCATION = "src/assets/logo.png"


# FIXME - Need to save the index for the most recently used file somewhere 
def end(gui, database, settings):
    # update_files(file_interface.containers)
    # database.close([c.file for c in file_interface.containers], settings)
    gui.window.destroy()

if __name__ == "__main__":
    ############################
    # Initialize GUI components
    ############################
    window = tk.Tk()
    window.title(TITLE)
    window.wm_iconphoto(False, make_icon(LOGO_LOCATION))
    ttk.Style(window).theme_use(THEME)
    vim_label = ttk.Label(window, anchor="w")

    #####################
    # Initialize Objects
    #####################
    settings = Settings()
    database = Database()
    vim_controller = VimController(vim_label)
    file_interface = FileInterface(window)
    gui = GUI(window, file_interface, vim_controller)

    ################################
    # Make final aesthetic changes
    ################################
    vim_controller.update_display()
    file_interface.notebook.grid(row=0, column=0, sticky="nsew")
    vim_controller.label.grid(row=1, column=0, sticky="ew")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.protocol("WM_DELETE_WINDOW", lambda: end(gui, database, settings))


    ################
    # Load settings
    ################
    data = database.load_settings()
    if data:
        colour, font_type, font_size = data
        settings.colour    = colour
        settings.font_type = font_type
        settings.font_size = font_size

    ##############################################
    # Initialize lambda function map for events
    ##############################################

    # vim_map = {
    #     "[0-9]*h" : lambda: h(file_interface),
    #     "[0-9]*j" : lambda: j(file_interface),
    #     "[0-9]*k" : lambda: k(file_interface),
    #     "[0-9]*l" : lambda: l(file_interface),
    #     "i"       : lambda: i(file_interface),
    #     "A"       : lambda: A(file_interface),
    #     "\^"      : lambda: hat(file_interface),
    #     "\$"      : lambda: dollar(file_interface),
    #     ":w"      : lambda: w(file_interface),
    #     ":q"      : lambda: q(file_interface),
    #     ":wq"     : lambda: wq(file_interface),
    #     ":q!"     : lambda: q_no_save(file_interface), 
    #     "gg"      : lambda: gg(file_interface),
    #     "G"       : lambda: G(file_interface)
    # }

    #################################
    # Load previous data and display
    #################################
    open_files = database.load_files()
    
    if len(open_files) == 0:
        file = File(path=None, 
                    name="New File",
                    rank=1, 
                    content=None, 
                    is_unsaved=True)
        open_files.append(file)

        file = File(path=None, 
                    name="New File 2",
                    rank=1, 
                    content=None, 
                    is_unsaved=True)
        open_files.append(file)
    
    for file in open_files: 
        gui.add_file(file, settings)

    ################
    # Start the GUI
    ################
    window.mainloop()
