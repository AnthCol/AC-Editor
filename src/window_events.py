from .file import File
from .codeview import make_codeview

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

def new(notebook, files, codeviews, settings):
    file = File(path=None, 
                name=determine_name(files),
                rank=determine_rank(files),
                content=None,
                is_unsaved=True) 
    codeview, frame = codeview.make_codeview(notebook, settings)
    codeview.fill_codeview(codeview, file)
    codeview.bind_codeview(codeview)
    files.append(file)
    codeviews.append(codeview)
    notebook.add(frame, text=file.name)

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
