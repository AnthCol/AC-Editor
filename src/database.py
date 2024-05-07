import os
import sqlite3
from file_datatypes import SavedFile, UnsavedFile

class Database():
    DB_NAME = "editor_data.db"
    DB_DIRECTORY = "../database/"

    def __init__(self):
        os.makedirs(self.DB_DIRECTORY, exist_ok=True)
        full_path = os.path.join(self.DB_DIRECTORY, self.DB_NAME)
        self.conn = sqlite3.connect(full_path)
        self.initialize_tables()

    def table_exists(self, name):
        fetch_table = self.conn.execute("SELECT name FROM sqlite_master WHERE name = ?", (name,))
        return fetch_table.fetchone() != None

    def prepare_table(self, name, table):
        if (not self.table_exists(name)):
            self.conn.execute(table)
        else:
            self.conn.execute("TRUNCATE TABLE ?", (name,))

    def initialize_tables(self):
        settings =      """ CREATE TABLE settings
                            (
                                COLOUR    TEXT    NOT NULL,
                                FONT_TYPE TEXT    NOT NULL, 
                                FONT_SIZE INTEGER NOT NULL
                            )
                        """
        saved_files =   """ CREATE TABLE saved_files
                            (
                                PATH TEXT    NOT NULL, 
                                RANK INTEGER NOT NULL
                            )
                        """
        unsaved_files = """ CREATE TABLE unsaved_files
                            (
                                CONTENT TEXT    NOT NULL,
                                RANK    INTEGER NOT NULL
                            )
                        """
        self.prepare_table("settings", settings)
        self.prepare_table("saved_files", saved_files)
        self.prepare_table("unsaved_files", unsaved_files)
        self.conn.commit()

    def load_files(self):
        
        return
    
    def insert_saved(self, file):
        self.conn.execute("INSERT INTO saved_files (PATH, RANK) VALUES (?, ?)", (file.path, file.rank))

    def insert_unsaved(self, file):
        self.conn.execute("INSERT INTO unsaved_files (CONTENT, RANK) VALUES (?, ?)", (file.content, file.rank))

    def save_files(self, file_info):
        for file in file_info:
            if isinstance(file, SavedFile):
                self.insert_saved(file)
            elif isinstance(file, UnsavedFile):
                self.insert_unsaved(file)
        self.conn.commit()

    def rewrite(self, file_info):
        os.remove(self.DB_PATH)
        self.save_files(file_info)

    def close(self):
        self.conn.close()

    def load_settings(self, settings):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM settings LIMIT 1")
        info = cursor.fetchone() 

        if info:
            colour, font_type, font_size = info
            settings.colour = colour
            settings.font_type = font_type
            settings.font_size = font_size