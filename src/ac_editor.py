import tkinter as tk

from tkinter     import ttk
from typing      import List
from chlorophyll import CodeView

from src.helper         import *
from src.types          import *
# from src.settings       import Settings
# from src.notebook       import show_last
# from src.codeview       import make_codeview, fill_codeview, bind_codeview
# from src.auxiliary      import make_icon
from src.vim_controller import VimController

# FIXME - Need to save the index for the most recently used file somewhere 
# need to write to database as well - see former commits 
def end(window):
    window.destroy()

if __name__ == "__main__":
    # Initialize GUI components
    window = tk.Tk()
    window.title("ac_editor")
    window.wm_iconphoto(False, make_icon("src/assets/logo.png"))
    ttk.Style(window).theme_use("clam")
    vim_label = ttk.Label(window, anchor="w")

    # Initialize Objects
    settings = Settings()
    database = Database()
    vim_status = VimController()

    # Indices of these will all correspond to one another
    # codeviews[1] = codeview for files[1]
    files : List[File] = []
    codeviews : List[CodeView] = []
    notebook = ttk.Notebook(window)

    vim_label.config(text=vim_status.message)
    notebook.grid(row=0, column=0, sticky="nsew")
    vim_label.grid(row=1, column=0, sticky="ew")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.protocol("WM_DELETE_WINDOW", lambda: end(window))
    bind_window(window)


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
        codeview, frame = make_codeview(notebook, settings)
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

    show_last(notebook)
    window.mainloop()
