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
    file = UnsavedFile("", len(containers), "New " + unsaved_rank(containers))
    file_inter.notebook.add(make_frame(file, settings, file_inter), text=pad(file.name))
    show_latest_page(file_inter.notebook)

def file_open(file_inter, settings, event=None):
    path = filedialog.askopenfilename()
    if path != "":
        file = SavedFile(path, determine_rank(file_inter.containers), os.path.basename(path))
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
    # If save == None, cancel was clicked and we do nothing. 

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


def interpret_command(vim_controller, label, event=None):
    vim_controller.buffer += str(event.char)
    vim_controller.interpret_buffer()

def esc_press(vim_controller, label, event=None):
    vim_controller.clear_buffer()
    if vim_controller.mode == vim_controller.INSERT:
        vim_controller.mode = vim_controller.NORMAL
        vim_controller.message = vim_controller.normal_message
        vim_controller.display_message(label)
    else:
        vim_controller.message = vim_controller.normal_message
        vim_controller.display_message(label)

########
# Other
########
def tab_change(window, file_inter, TITLE, event=None):
    index = file_inter.notebook.index(file_inter.notebook.select())
    file = file_inter.containers[index].file
    path = file.path if isinstance(file, SavedFile) else file.name
    window.title(TITLE + " - " + path)
