import os
import sqlite3

class Database():
    DB_PATH = "./database/editor_data.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.create_tables()

    def table_exists(self, name):
        fetch_table = self.conn.execute("SELECT name FROM sqlite_master WHERE name = ?", (name,))
        return fetch_table.fetchone() != None

    def create_tables(self):
        if (not self.table_exists("settings")): 
            Settings =  """ CREATE TABLE settings
                            (
                                COLOUR    VARCHAR(32) NOT NULL,
                                FONT_TYPE VARCHAR(32) NOT NULL, 
                                FONT_SIZE INTEGER     NOT NULL
                            )
                        """
            self.conn.execute(Settings)

        if (not self.table_exists("saved_files")):
            saved_files =    """ CREATE TABLE saved_files
                                (
                                    PATH TEXT    NOT NULL, 
                                    RANK INTEGER NOT NULL
                                )
                            """
            self.conn.execute(saved_files)

        if (not self.table_exists("unsaved_files")):
            unsaved_files = """ CREATE TABLE unsaved_files
                                (
                                    CONTENT TEXT    NOT NULL,
                                    RANK    INTEGER NOT NULL
                                )
                            """

        self.conn.commit()

    def save(self, settings):
        return

    def load_files(self, file_info):

        return

    def save_files(self, file_info):

        return

    def rewrite(self, file_info):
        os.remove(self.DB_PATH)
        self.save_files(file_info)
        return


