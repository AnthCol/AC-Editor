from src.settings import Settings
from src.gui import GUIManager
from src.database import Database
import tkinter as tk

if __name__ == "__main__": 
    gui_manager = GUIManager(tk.Tk(), Settings(), Database())
    gui_manager.start() 
