__version__ = "3.0.0"
from .db import Database, Table

db = Database()

__all__ = ["Database", "Table"]
