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

    file_save_as(file_inter) if save else remove_file(file_inter, index)

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



############
# Edit Menu
############
def cut(event=None):
    return

def copy(event=None):
    return

def paste(event=None):
    return

def select_all(event=None):
    return

################
# Settings Menu
################
def theme(event=None):
    return

def font_size(event=None):
    return

def tab_size(event=None):
    return

def line_endings(event=None):
    return

################
# Vim Events
################
def i_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        vim.mode = vim.INSERT
    
def h_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        return
        
def j_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        return

def k_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        return

def l_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        return
    
def shift_a_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        return

def shift_hat_press(vim, event=None):
    return

def shift_dollar_press(vim, event=None):
    return

def number_press(vim, event=None):
    if vim.mode == vim.NORMAL:
        vim.buffer += event.char

########
# Other
########
def tab_change(window, file_inter, event=None):
    index = file_inter.notebook.index(file_inter.notebook.select())
    file = file_inter.containers[index].file
    path = file.path if isinstance(file, SavedFile) else file.name
    window.title("ac_editor - " + path)

def close(event=None):
    return