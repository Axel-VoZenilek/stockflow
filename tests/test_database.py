import os 
os.environ["STOCKFLOW_ENV"] = "test"
from database.schema import create_db       
from database.connection import DatabaseConnection
import unittest
import sqlite3
from common.config import get_database_path
DB_TEST_PATH = get_database_path()
class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseConnection()

    def tearDown(self):
        # Close the database connection after each test
        self.db.close()
        os.remove(DB_TEST_PATH)

    def test_execute_query(self):
        # Test executing a simple query
        result = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='product';")
        table_exists = result.fetchone() is not None
        self.assertTrue(table_exists, "The 'product' table should exist in the database.")
    def test_contraint_violation(self):
        # Test foreign key constraint violation
        self.db.execute("INSERT INTO product (label,sku,category,sale_price) VALUES (?, ?, ?, ?);", ('Test Product',"test_sku",1,10))
        self.db.execute("INSERT INTO stocks (id_product, store_count,reserve_count) VALUES (?, ?,?);", (1, 100,10))
        self.db.execute("INSERT INTO movements (id_stock, type_movement,stock_before,stock_after,date_move,is_reserve,quantity_moves) VALUES (?, ?, ?, ?, ?, ?, ?);", (1, 1, 100, 90, 1234567890, 0, -10))
        self.assertIsNotNone(self.db.execute("SELECT * FROM movements WHERE id_stock = ?;", (1,)).fetchone() is None, "The movement should be inserted successfully.")
        self.assertRaises(sqlite3.IntegrityError, self.db.execute, "INSERT INTO movements (id_stock, type_movement,stock_before,stock_after,date_move,is_reserve,quantity_moves) VALUES (?, ?, ?, ?, ?, ?, ?);", (1, 5, 100, 90, 1234567890, 0, 10))
        self.assertRaises(sqlite3.IntegrityError, self.db.execute, "INSERT INTO movements (id_stock, type_movement,stock_before,stock_after,date_move,is_reserve,quantity_moves) VALUES (?, ?, ?, ?, ?, ?, ?);", (1, 5, 100, 90, 1234567890, 0, 10))
if __name__ == '__main__':
    unittest.main()