import os
import sqlite3
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')
SCHEMA = open(SCHEMA_PATH, 'r').read()
DB_PATH = os.path.join(os.path.dirname(__file__), 'stockflow.db')
def create_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA)
    conn.commit()
    conn.close()