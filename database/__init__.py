"""
Database package initialization.
Exports the main database classes and connection utilities.
"""

from .connection import DatabaseConnection
from .auth_db import AuthDB
from .data_db import DataDB
from .schema import CREATE_TABLES_QUERIES

__all__ = [
    'DatabaseConnection',
    'AuthDB',
    'DataDB',
    'CREATE_TABLES_QUERIES'
]