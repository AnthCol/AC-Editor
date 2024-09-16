import os
import sqlite3
from .file import File


class Database():
    DB_DIRECTORY = "./database/"
    DB_PATH = "./database/editor_data.db"

    def __init__(self):
        os.makedirs(self.DB_DIRECTORY, exist_ok=True)
        self.conn = sqlite3.connect(self.DB_PATH)
        self.initialize_tables()

    def table_exists(self, name):
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE name = ?", (name,))
        return cursor.fetchone() != None

    def create_table(self, table, name):
        if not self.table_exists(name):
            self.conn.execute(table)

    # Not injection, hardcoded function calls. 
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
        files = """ CREATE TABLE files
                            (
                                PATH       TEXT    NOT NULL,
                                NAME       TEXT    NOT NULL, 
                                RANK       INTEGER NOT NULL,
                                CONTENT    TEXT    NOT NULL,
                                IS_UNSAVED INTEGER NOT NULL
                            )
                        """
        self.create_table(settings, "settings")
        self.create_table(files, "files")
        self.conn.commit()

    def load_files(self):
        cursor = self.conn.execute("SELECT * FROM files")
        files = cursor.fetchall()

        file_list = []

        for file in files:
            path, name, rank, content, is_unsaved = file    
            file_list.append(File(path, name, rank, content, is_unsaved))

        return file_list

    def insert_file(self, file):
        data = (file.path, file.name, file.rank, file.content, file.is_unsaved)
        self.conn.execute("INSERT INTO files (PATH, NAME, RANK, CONTENT, IS_UNSAVED)", data)

    # FIXME maybe in the future we don't bother clearing the table and find a way 
    # to update them instead?
    def save_files(self, file_info):
        self.clear_table("files")
        for file in file_info:
            self.insert_file(file)
        self.conn.commit()

    def save_settings(self, settings):
        self.clear_table("settings")
        data = (settings.colour, settings.font_type, settings.font_size)
        self.conn.execute("INSERT INTO settings (COLOUR, FONT_TYPE, FONT_SIZE) VALUES (?, ?, ?)", data)
        self.conn.commit()

    def close(self, file_info, settings):
        self.save_files(file_info)
        self.save_settings(settings)
        self.conn.close()

    def load_settings(self):
        cursor = self.conn.execute("SELECT * FROM settings LIMIT 1")
        return cursor.fetchone()
    
