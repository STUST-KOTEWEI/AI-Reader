"""
Database Persistence Layer

Provides database abstraction for data persistence.
"""

from .database_manager import (
    DatabaseAdapter,
    SQLiteConnection,
    DatabaseManager,
    get_database_manager
)

__all__ = [
    'DatabaseAdapter',
    'SQLiteConnection',
    'DatabaseManager',
    'get_database_manager'
]
