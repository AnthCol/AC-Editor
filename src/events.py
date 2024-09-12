import re 
import os

import tkinter as tk


from tkinter         import filedialog

from .auxiliary      import pad
from .gui_helpers    import make_frame, show_latest_page
from .file_helpers   import unsaved_rank, determine_rank, remove_file, codeview_contents
from .file_datatypes import SavedFile, UnsavedFile



############
# File Menu
############
def file_new(file_inter, settings, event=None):
    containers = file_inter.containers
    rank = determine_rank(file_inter.containers)
    # Rank in file vs rank in notebook are different. 
    file = UnsavedFile("", rank, "New " + unsaved_rank(containers))
    frame = make_frame(file, settings, file_inter)
    if frame != None:
        file_inter.notebook.add(make_frame(file, settings, file_inter), text=pad(file.name))
        show_latest_page(file_inter.notebook)

def file_open(file_inter, settings, event=None):
    path = filedialog.askopenfilename()
    if path != "":
        rank = determine_rank(file_inter.containers)
        file = SavedFile(path, rank, os.path.basename(path))
        frame = make_frame(file, settings, file_inter)
        if frame != None:
            file_inter.notebook.add(make_frame(file, settings, file_inter), text=pad(file.name))
            show_latest_page(file_inter.notebook)

def file_close(file_inter, settings, event=None):
    index = file_inter.notebook.index(file_inter.notebook.select())
    file = file_inter.containers[index].file
    content = codeview_contents(file_inter.containers[index].codeview)

    save = False 

    if isinstance(file, UnsavedFile) and content != "":
        save = tk.messagebox.askyesnocancel("Save File", "Do you want to save this file?")

    if save == True:
        file_save_as(file_inter)
    elif save == False:
        remove_file(file_inter, index)
    # elif save == None, cancel was clicked and we do nothing. 

    if len(file_inter.containers) == 0:
        file_new(file_inter, settings)


def file_save(file_inter, event=None):
    index = file_inter.notebook.index(file_inter.notebook.select())
    container = file_inter.containers[index]
    file = container.file

    if isinstance(file, SavedFile):
        with open(file.path, "w") as f:
            f.write(codeview_contents(container.codeview))
    else:
        file_save_as(file_inter)

# FIXME creates a new file, but doesn't get rid of the old one. 
def file_save_as(file_inter, window, TITLE, event=None):
    path = filedialog.asksaveasfilename()
    if path != "":
        index = file_inter.notebook.index(file_inter.notebook.select())
        old = file_inter.containers[index]
        new = SavedFile(path, old.file.rank, os.path.basename(path))
        file_inter.containers[index].file = new
        file_inter.notebook.tab(index, text=pad(new.name))
        with open(path, "w") as f:
            f.write(codeview_contents(file_inter.containers[index].codeview))
        window.title(TITLE + " - " + path)

################
# Vim Events
################

VALID_COMMANDS = {
    "[0-9]*h" : lambda: 10,
    "[0-9]*j" : lambda: 10,
    "[0-9]*k" : lambda: 10,
    "[0-9]*l" : lambda: 10,
    "i"       : lambda: 10,
    "A"       : lambda: 10,
    "\^"      : lambda: 10,
    "\$"      : lambda: 10, 
    ":w"      : lambda: 10,
    ":q"      : lambda: 10, 
    ":wq"     : lambda: 10, 
    ":q!"     : lambda: 10, 
    "gg"      : lambda: 10,
    "G"       : lambda: 10
}


def handle_command(vim_controller, file_interface, event=None):
    vim_controller.append_buffer(str(event.char))
    vim_controller.update_display()
    interpret_buffer(vim_controller, file_interface)

def esc_press(vim_controller, event=None):
    vim_controller.switch_normal()

def return_press(vim_controller, file_interface, event=None):
    interpret_buffer(vim_controller, file_interface)

def backspace_press(vim_controller, event=None):
    vim_controller.delete_char()

def is_valid_command(command):
    for regex in VALID_COMMANDS:
        print("printing regex: " + regex + " and command: " + command)
        if re.match(regex, command):
            return (True, regex)
    return (False, None)

def interpret_buffer(vim_controller, file_interface):
    buffer = vim_controller.get_buffer()
    values = is_valid_command(buffer)
    valid = values[0]
    regex = values[1]

    if valid:
        vim_controller.reset_buffer()
        print("printing command and regex: " + buffer + " " + regex)


########
# Other
########
def tab_change(window, file_inter, TITLE, event=None):
    index = file_inter.notebook.index(file_inter.notebook.select())
    file = file_inter.containers[index].file
    path = file.path if isinstance(file, SavedFile) else file.name
    window.title(TITLE + " - " + path)
