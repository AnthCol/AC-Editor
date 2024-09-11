import tkinter as tk

from tkinter         import ttk
from chlorophyll     import CodeView

from .file_helpers   import determine_lexer
from .code_container import CodeContainer
from .file_datatypes import SavedFile

def make_frame(file, settings, file_inter):
    frame = ttk.Frame(file_inter.notebook)

    codeview = CodeView(frame, 
                        insertwidth=10, 
                        color_scheme=settings.colour, 
                        font=(settings.font_type, settings.font_size), 
                        lexer=determine_lexer(file))

    # Add more error checking later (make sure file actually exists)
    if isinstance(file, SavedFile):
        try:
            with open(file.path) as f:
                content = f.read()
            codeview.insert(tk.END, content)
        except Exception as e:
            tk.messagebox.showerror("Error", "Invalid file type.")
            return None
    else:
        codeview.insert(tk.END, file.content)

    codeview.pack(fill="both", expand=True)

    file_inter.containers.append(CodeContainer(file=file, codeview=codeview))
    return frame

def last_page_index(notebook):
    return notebook.index("end") - 1

def show_latest_page(notebook):
    notebook.select(last_page_index(notebook))

