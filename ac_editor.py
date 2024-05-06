import tkinter as tk
import chlorophyll

# def create_submenu(menubar, label):
#     submenu = tk.Menu(menubar)
#     submenu.add_command(label=label)
#     return menubar

# def add_menus(gui):
#     menubar = tk.Menu(gui)
#     gui.config(menu=menubar) 
#     menubar = create_submenu(menubar, "File")
#     menubar = create_submenu(menubar, "Edit")
#     menubar = create_submenu(menubar, "Settings")
#     return gui

def initialize_gui():
    gui = tk.Tk()
    gui.title("ac_editor")

    menubar = tk.Menu(gui)

    gui.config(menu=menubar)

    file_menu = tk.Menu(menubar)
    edit_menu = tk.Menu(menubar)
    settings_menu = tk.Menu(menubar)

    file_menu.add_command(label = "New")
    file_menu.add_command(label = "Open")
    file_menu.add_command(label = "Save As")
    file_menu.add_command(label = "Rename")

    edit_menu.add_command(label = "Cut")
    edit_menu.add_command(label = "Copy")
    edit_menu.add_command(label = "Paste")
    edit_menu.add_command(label = "Select All")

    settings_menu.add_command(label = "Theme")
    settings_menu.add_command(label = "Tab Size")
    settings_menu.add_command(label = "Line Endings")

    menubar.add_cascade(label = "File", menu=file_menu)
    menubar.add_cascade(label = "Edit", menu=edit_menu)
    menubar.add_cascade(label = "Settings", menu=settings_menu)

    return gui


if (__name__ == "__main__"):
    window = initialize_gui()
    window.mainloop()
