import sqlite3
import pathlib

PATH_DB = pathlib.Path(__file__).parent / 'stockflow.db'
class DatabaseConnection:
    def __init__(self, db_path=PATH_DB):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

    def close(self):
        self.conn.close()