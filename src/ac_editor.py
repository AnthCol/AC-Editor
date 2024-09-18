import re
import tkinter as tk

from tkinter     import ttk, PhotoImage
from typing      import List
from chlorophyll import CodeView

from classes.file           import File
from classes.database       import Database
from classes.settings       import Settings
from classes.vim_controller import VimController

##########
# Globals
##########
WINDOW_EVENTS = {
    "new"        : lambda event: new(),
    "load"       : lambda event: load(),
    "save"       : lambda event: save(),
    "save_as"    : lambda event: save_as(), 
    "close"      : lambda event: close(), 
    "tab_change" : lambda event: tab_change(),
    "vim"        : lambda event: vim(event), 
    "esc"        : lambda event: esc(), 
    "ret"        : lambda event: ret(),
    "back"       : lambda event: back()
}

VIM_CHARS = [
    "<i>", 
    "<h>", 
    "<j>", 
    "<k>", 
    "<l>", 
    "<g>",
    "<Shift-A>", 
    "<Shift-G>",
    "<Shift-asciicircum>", 
    "<Shift-dollar>",
    "0", 
    "1", 
    "2", 
    "3", 
    "4",
    "5", 
    "6", 
    "7", 
    "8", 
    "9"
]

VIM_REGEX = {
    "[0-9]*h" : lambda: h(),
    "[0-9]*j" : lambda: j(),
    "[0-9]*k" : lambda: k(),
    "[0-9]*l" : lambda: l(),
    "i"       : lambda: i(),
    "A"       : lambda: A(),
    "\\^"     : lambda: hat(),
    "\\$"     : lambda: dollar(), 
    ":w"      : lambda: w(),
    ":q"      : lambda: q(save=True), 
    ":wq"     : lambda: wq(), 
    ":q!"     : lambda: q(save=False), 
    "gg"      : lambda: gg(),
    "G"       : lambda: G()
}

# Global GUI state (I don't like it either)
window = tk.Tk()
settings = Settings()
database = Database()
vim_status = VimController(ttk.Label(window, anchor="w"))
files : List[File] = []
codeviews : List[CodeView] = []
notebook = ttk.Notebook(window)


############
# Functions
############
def bind_codeview(codeview):
    for char in VIM_CHARS:
        codeview.bind(char, WINDOW_EVENTS["vim"])
    codeview.bind("<Escape>", WINDOW_EVENTS["esc"])
    codeview.bind("<Return>", WINDOW_EVENTS["ret"])
    codeview.bind("<BackSpace>", WINDOW_EVENTS["back"])

def make_codeview():
    global notebook
    global settings
    frame = ttk.Frame(notebook)
    codeview = CodeView(frame,
                        insertwidth=10,
                        color_scheme=settings.colour,
                        font=(settings.font_type, settings.font_size))
    codeview.pack(fill="both", expand=True)
    return (codeview, frame)


def fill_codeview(codeview, file):
    failed = False
    content = file.content
    if file.is_unsaved == False:
        try:
            with open(file.path) as f:
                content = f.read()
        except Exception as e:
            tk.messagebox.showerror("Error", "Invalid file type.")
            failed = True
    if not failed:
        codeview.insert(tk.END, content)


def extract_file(db_file):
    path, name, rank, content, is_unsaved = db_file
    file = File(path=path,
                name=name,
                rank=rank,
                content=content,
                is_unsaved=is_unsaved)
    return file

def determine_name():
    global files
    return ""

def determine_rank():
    global files
    return 1

def new():
    global notebook
    global settings
    global codeviews
    global files
    file = File(path=None, 
                name=determine_name(),
                rank=determine_rank(),
                content=None,
                is_unsaved=True) 
    codeview, frame = make_codeview()
    fill_codeview(codeview, file)
    bind_codeview(codeview)
    files.append(file)
    codeviews.append(codeview)
    notebook.add(frame, text=file.name)

def end():
    global window
    window.destroy()

def show_last():
    global notebook
    notebook.select(notebook.index("end") - 1)

def update_title(file):
    global window
    title = file.name if file.is_unsaved else file.path
    window.title("ac_editor - " + title)

def make_icon(path):
    return PhotoImage(file=path)

def load():
    return
def save():
    return
def save_as():
    return
def close():
    return
def tab_change():
    return

def is_valid_vim(command):
    for regex in VIM_REGEX:
        if re.match(regex, command):
            return (True, regex)
    return (False, None)

def process_vim(command):
    global vim_status
    values = is_valid_vim(command)
    valid = values[0]
    regex = values[1]

    print("printing in process vim: " + str(valid) + " " + str(regex))
    if valid:
        VIM_REGEX[regex]()
        vim_status.reset_buffer()

# Called whenever any of the valid vim characters are pressed
def vim(event=None):
    global vim_status
    vim_status.append_buffer(event.char)
    vim_status.update_display()
    process_vim(vim_status.command_buffer)

########################
# Vim Related Functions
########################
def esc():
    global vim_status
    vim_status.switch_normal()

def ret():
    global vim_status
    process_vim(vim_status.command_buffer)

def back(event=None):
    global vim_status
    vim_status.delete_char()



######################
# VIM_REGEX functions
######################
def h():
    return
def j():
    print("in j function")
    return
def k():
    return
def l():
    return
def i():
    return
def A():
    return
def hat():
    return
def dollar():
    return
def w():
    return
def q(save):
    return
def wq():
    return
def gg():
    return
def G():
    return


#######
# Main
#######
if __name__ == "__main__":
    window.title("ac_editor")
    icon = make_icon("src/assets/logo.png")
    window.wm_iconphoto(False, icon)
    ttk.Style(window).theme_use("clam")

    vim_status.update_display()
    notebook.grid(row=0, column=0, sticky="nsew")
    vim_status.label_grid()
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.protocol("WM_DELETE_WINDOW", lambda: end())

    window.bind("<Control-s>", WINDOW_EVENTS["save"])
    window.bind("<Control-Alt-s>", WINDOW_EVENTS["save_as"])
    window.bind("<Control-q>", WINDOW_EVENTS["close"])
    window.bind("<Control-o>", WINDOW_EVENTS["load"])
    window.bind("<Control-n>", WINDOW_EVENTS["new"])
    notebook.bind("<<NotebookTabChanged>>", WINDOW_EVENTS["tab_change"])

    data = database.load_settings()
    if data:
        colour, font_type, font_size = data
        settings.colour    = colour
        settings.font_type = font_type
        settings.font_size = font_size

    db_files = database.load_files()

    if len(db_files) == 0:
        file = File(path=None, 
                    name="New 1",
                    rank=1,
                    content=None,
                    is_unsaved=True)
        codeview, frame = make_codeview()
        fill_codeview(codeview, file)
        bind_codeview(codeview)

        files.append(file)
        codeviews.append(codeview)
        notebook.add(frame, text=file.name)
    else:
        for db_file in db_files: 
            codeview, frame = make_codeview(notebook, settings)        
            file = extract_file(db_file)
            fill_codeview(codeview, file)
            bind_codeview(codeview)
            files.append(file)
            codeviews.append(codeview)
            notebook.add(frame, text=file.name)

    show_last()
    window.mainloop()


