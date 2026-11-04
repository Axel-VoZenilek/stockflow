import os
import sqlite3
from common.config import get_database_path
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')
SCHEMA = open(SCHEMA_PATH, 'r').read()
DB_PATH = get_database_path()
def create_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA)
    conn.commit()
    conn.close()