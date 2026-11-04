import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def get_database_path():
    if os.getenv("STOCKFLOW_ENV") == "test":
        return BASE_DIR / "database" / "test_stockflow.db"

    return BASE_DIR / "database" / "stockflow.db"