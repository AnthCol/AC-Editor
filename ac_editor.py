from settings import Settings
from gui import initialize_gui

if (__name__ == "__main__"):
    gui = initialize_gui(Settings())
    gui.mainloop()
    
