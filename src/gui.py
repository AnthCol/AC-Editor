from PIL         import Image, ImageTk
from tkinter     import ttk
from chlorophyll import CodeView

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
    "<Shift-dollar>"
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

WINDOW_EVENTS = {
    "new"        : lambda event: new(), 
    "load"       : lambda event: load(),
    "save"       : lambda event: save(),
    "save_as"    : lambda event: save_as(), 
    "close"      : lambda event: close(), 
    "tab_change" : lambda event: tab_change(),
    "vim"        : lambda event: vim(), 
    "esc"        : lambda event: esc(), 
    "ret"        : lambda event: ret(),
    "back"       : lambda event: back()
}

def determine_name(files):
    return
def determine_rank(files):
    return
def new():
    return
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
def vim():
    return
def esc():
    return
def ret():
    return
def back():
    return

def bind_window(window):
    return

def make_codeview(notebook, settings):
    frame = ttk.Frame(notebook)
    codeview = CodeView(frame,
                        insertwidth=10,
                        color_scheme=settings.colour,
                        font=(settings.font_type, settings.font_size))
    codeview.pack(fill="both", expand=True)
    return (codeview, frame)

def fill_codeview(codeview, file):
    return

def bind_codeview(codeview):
    for char in VIM_CHARS:
        codeview.bind(char, WINDOW_EVENTS["vim"])
    codeview.bind("<Escape>", WINDOW_EVENTS["esc"])
    codeview.bind("<Return>", WINDOW_EVENTS["ret"])
    codeview.bind("<BackSpace>", WINDOW_EVENTS["back"])
    return

def make_icon(path):
    with Image.open(path) as image:
        icon = ImageTk.PhotoImage(image) 
    return icon

def show_last(notebook):
    return