import sqlite3
import pathlib
from .schema import create_db
from common.config import get_database_path
class DatabaseConnection:
    def __init__(self):
        if not pathlib.Path(get_database_path()).exists():
            create_db()
        self.conn = sqlite3.connect(get_database_path())
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