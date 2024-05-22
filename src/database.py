import os
import sqlite3
from .file_datatypes import SavedFile, UnsavedFile


class Database():
    DB_DIRECTORY = "./database/"
    DB_PATH = "./database/editor_data.db"

    def __init__(self):
        os.makedirs(self.DB_DIRECTORY, exist_ok=True)
        self.conn = sqlite3.connect(self.DB_PATH)
        self.initialize_tables()

    def table_exists(self, name):
        fetch_table = self.conn.execute("SELECT name FROM sqlite_master WHERE name = ?", (name,))
        return fetch_table.fetchone() != None

    def create_table(self, table, name):
        if (not self.table_exists(name)):
            self.conn.execute(table)

    # Note injection, hardcoded function calls. 
    def clear_table(self, name):
        self.conn.execute("DELETE FROM " + name)

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
        self.create_table(settings, "settings")
        self.create_table(saved_files, "saved_files")
        self.create_table(unsaved_files, "unsaved_files")
        self.conn.commit()

    def load_files(self):
        cursor = self.conn.execute("SELECT * FROM saved_files")
        saved_files = cursor.fetchall()

        cursor = self.conn.execute("SELECT * FROM unsaved_files")
        unsaved_files = cursor.fetchall()

        file_list = [None] * (len(saved_files) + len(unsaved_files))

        print(saved_files)
        print(unsaved_files)

        # Rank starts at 1, indices start at 0
        for file in saved_files:
            path, rank = file
            file_list[rank - 1] = SavedFile(path, rank)

        for file in unsaved_files:
            content, rank = file
            file_list[rank - 1] = UnsavedFile(content, rank)

        print("printing file_list: " + str(file_list))

        return file_list
    
    def insert_saved(self, file):
        self.conn.execute("INSERT INTO saved_files (PATH, RANK) VALUES (?, ?)", (file.path, file.rank))

    def insert_unsaved(self, file):
        self.conn.execute("INSERT INTO unsaved_files (CONTENT, RANK) VALUES (?, ?)", (file.content, file.rank))

    def save_files(self, file_info):
        self.clear_table("saved_files")
        self.clear_table("unsaved_files")

        for file in file_info:
            if isinstance(file, SavedFile):
                self.insert_saved(file)
            elif isinstance(file, UnsavedFile):
                self.insert_unsaved(file)
        
        self.conn.commit()

    def close(self, file_info):
        # print("IN DATABASE PRINTING FILE INFO:")
        # print(file_info)
        self.save_files(file_info)
        self.conn.close()

    def load_settings(self):
        cursor = self.conn.execute("SELECT * FROM settings LIMIT 1")
        info = cursor.fetchone() 
        return info 
    
