import os
import sys
import pygments.lexers

import tkinter as tk

from tkinter               import ttk

from src.events       import *
from src.auxiliary    import make_icon, pad
from src.gui_helpers  import make_frame
from src.file_helpers import update_files, unsaved_rank

from src.classes.file           import File
from src.classes.settings       import Settings
from src.classes.database       import Database
from src.classes.file_interface import FileInterface
from src.classes.vim_controller import VimController

###########################################################
# Constants 
# (FIXME, theme should be moved to Settings in the future)
###########################################################
TITLE = "ac_editor"
THEME = "clam"
LOGO_LOCATION = "src/assets/logo.png"


# FIXME - Need to save the index for the most recently used file somewhere 
def end(window, database, settings, file_interface):
    # update_files(file_interface.containers)
    # database.close([c.file for c in file_interface.containers], settings)
    window.destroy()

if __name__ == "__main__":
    ############################
    # Initialize GUI components
    ############################
    window = tk.Tk()
    window.title(TITLE)
    window.wm_iconphoto(False, make_icon(LOGO_LOCATION))
    ttk.Style(window).theme_use(THEME)
    #vim_label = ttk.Label(window, anchor="w")

    # #################
    # # Necessary Data
    # #################
    settings = Settings()
    database = Database()
    # vim_controller = VimController(vim_label)
    # file_interface = FileInterface(window)

    # ###############################
    # # Make final aesthetic changes
    # ###############################
    # vim_controller.update_display()
    # file_interface.notebook.grid(row=0, column=0, sticky="nsew")
    # vim_label.grid(row=1, column=0, sticky="ew")
    # window.grid_rowconfigure(0, weight=1)
    # window.grid_columnconfigure(0, weight=1)
 
    # ################
    # # Load settings
    # ################
    # data = database.load_settings()
    # if data:
    #     colour, font_type, font_size = data
    #     settings.colour    = colour
    #     settings.font_type = font_type
    #     settings.font_size = font_size

    # ############################################
    # # Initialize lambda function map for events
    # ############################################

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


    # # FIXME, figure out which ones actually need the events 
    # event_map = {
    #     # Editor Shorcuts
    #     "new"          : lambda event: file_new(file_interface, settings),
    #     "open"         : lambda event: file_open(file_interface, settings, event),
    #     "save"         : lambda event: file_save(file_interface, event),
    #     "save_as"      : lambda event: file_save_as(file_interface, window, TITLE),
    #     "close"        : lambda event: file_close(file_interface, settings),
    #     "end"          : lambda: end(window, database, settings, file_interface),
    #     "tab_change"   : lambda event: tab_change(window, file_interface, TITLE), 
    #     # Vim Commands
    #     "vim"          : lambda event: handle_command(vim_controller, file_interface, vim_map, event),
    #     "esc"          : lambda event: esc_press(vim_controller),
    #     "return"       : lambda event: return_press(vim_controller, file_interface),
    #     "back"         : lambda event: backspace_press(vim_controller)
    # } 

    # #####################################
    # # Initialize Non-Vim Window Bindings
    # #####################################
    # window.protocol("WM_DELETE_WINDOW", event_map["end"])
    # window.bind("<Control-s>", event_map["save"])
    # window.bind("<Control-Alt-s>", event_map["save_as"])
    # window.bind("<Control-q>", event_map["close"])
    # window.bind("<Control-o>", event_map["open"])
    # window.bind("<Control-n>", event_map["new"])
    # file_interface.notebook.bind("<<NotebookTabChanged>>", event_map["tab_change"])


    # #################################
    # # Load previous data and display
    # #################################
    # open_files = database.load_files()
    
    # if len(open_files) == 0:
    #     open_files.append(UnsavedFile("", 1, "New " + unsaved_rank(file_interface.containers)))
    
    # for f in open_files: 
    #     file_interface.notebook.add(make_frame(f, settings, file_interface), text=pad(f.name))

    # ##########################
    # # Initialize Vim Bindings
    # ########################## 
    # vim_commands = [
    #     "<i>",
    #     "<h>",
    #     "<j>",
    #     "<k>",
    #     "<l>",
    #     "<g>",
    #     "<Shift-A>",
    #     "<Shift-G>",
    #     "<Shift-asciicircum>",
    #     "<Shift-dollar>"
    #     "0",
    #     "1",
    #     "2",
    #     "3",
    #     "4",
    #     "5",
    #     "6",
    #     "7",
    #     "8",
    #     "9"
    # ]

    # for c in file_interface.containers:
    #     for command in vim_commands:
    #         c.codeview.bind(command, event_map["vim"])
    #     # It is easier to treat these on their own.
    #     c.codeview.bind("<Escape>", event_map["esc"]) 
    #     c.codeview.bind("<Return>", event_map["return"])
    #     c.codeview.bind("<BackSpace>", event_map["back"])

    # ################
    # # Start the GUI
    # ################
    window.mainloop()
