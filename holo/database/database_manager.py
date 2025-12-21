"""
Database Persistence Layer

Provides database abstraction for data persistence.
Uses SQLite for local storage and can be extended to other databases.
"""

from typing import Dict, Any, List, Optional, TypeVar, Generic
from dataclasses import dataclass, asdict
from datetime import datetime
from abc import ABC, abstractmethod
import json
import sqlite3
import os


T = TypeVar('T')


class DatabaseAdapter(ABC, Generic[T]):
    """Abstract database adapter interface."""
    
    @abstractmethod
    def create(self, item: T) -> T:
        """Create a new item."""
        pass
    
    @abstractmethod
    def read(self, item_id: str) -> Optional[T]:
        """Read an item by ID."""
        pass
    
    @abstractmethod
    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[T]:
        """Update an item."""
        pass
    
    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Delete an item."""
        pass
    
    @abstractmethod
    def list_all(self, **filters) -> List[T]:
        """List all items with optional filters."""
        pass


class SQLiteConnection:
    """SQLite database connection manager."""
    
    def __init__(self, db_path: str = "data/ai_reader.db"):
        self.db_path = db_path
        self._ensure_directory()
        self.connection: Optional[sqlite3.Connection] = None
    
    def _ensure_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def connect(self) -> sqlite3.Connection:
        """Get database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """Execute a query with multiple parameter sets."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor
    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetch one result."""
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Fetch all results."""
        cursor = self.execute(query, params)
        return cursor.fetchall()


class DatabaseManager:
    """Manages database operations and schema."""
    
    def __init__(self, db_path: str = "data/ai_reader.db"):
        self.connection = SQLiteConnection(db_path)
        self._initialized = False
    
    def initialize(self):
        """Initialize database schema."""
        if self._initialized:
            return
        
        # Users table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                is_active INTEGER DEFAULT 1,
                role TEXT DEFAULT 'user'
            )
        """)
        
        # Profiles table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                user_id TEXT PRIMARY KEY,
                display_name TEXT,
                accessibility_settings TEXT,
                preferences TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Reading history table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS reading_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_title TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                progress REAL DEFAULT 0,
                duration_seconds INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Bookmarks table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                bookmark_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_title TEXT NOT NULL,
                position TEXT,
                note TEXT,
                tags TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Favorites table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                favorite_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_title TEXT NOT NULL,
                content_type TEXT DEFAULT 'book',
                rating INTEGER DEFAULT 0,
                added_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Comments table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                comment_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT,
                likes INTEGER DEFAULT 0,
                parent_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Notifications table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                created_at TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                action_url TEXT,
                metadata TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Content catalog table
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS content (
                content_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                genre TEXT,
                tags TEXT,
                rating REAL DEFAULT 0,
                popularity_score REAL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        
        # Create indexes
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON reading_sessions(user_id)")
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_bookmarks_user ON bookmarks(user_id)")
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id)")
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_comments_content ON comments(content_id)")
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)")
        
        self._initialized = True
    
    def close(self):
        """Close database connection."""
        self.connection.close()
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Create a new user."""
        try:
            self.connection.execute("""
                INSERT INTO users (user_id, username, email, password_hash, created_at, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_data['user_id'],
                user_data['username'],
                user_data['email'],
                user_data['password_hash'],
                user_data.get('created_at', datetime.now().isoformat()),
                user_data.get('role', 'user')
            ))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        row = self.connection.fetchone(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return dict(row) if row else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        row = self.connection.fetchone(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        return dict(row) if row else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        row = self.connection.fetchone(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        return dict(row) if row else None
    
    # Reading session operations
    def add_reading_session(self, session_data: Dict[str, Any]) -> bool:
        """Add a reading session."""
        try:
            self.connection.execute("""
                INSERT INTO reading_sessions 
                (session_id, user_id, content_id, content_title, started_at, ended_at, progress, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_data['session_id'],
                session_data['user_id'],
                session_data['content_id'],
                session_data['content_title'],
                session_data['started_at'],
                session_data.get('ended_at'),
                session_data.get('progress', 0),
                session_data.get('duration_seconds', 0)
            ))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get reading sessions for a user."""
        rows = self.connection.fetchall(
            "SELECT * FROM reading_sessions WHERE user_id = ? ORDER BY started_at DESC LIMIT ?",
            (user_id, limit)
        )
        return [dict(row) for row in rows]
    
    # Bookmark operations
    def add_bookmark(self, bookmark_data: Dict[str, Any]) -> bool:
        """Add a bookmark."""
        try:
            tags_json = json.dumps(bookmark_data.get('tags', []))
            self.connection.execute("""
                INSERT INTO bookmarks 
                (bookmark_id, user_id, content_id, content_title, position, note, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                bookmark_data['bookmark_id'],
                bookmark_data['user_id'],
                bookmark_data['content_id'],
                bookmark_data['content_title'],
                bookmark_data.get('position', ''),
                bookmark_data.get('note', ''),
                tags_json,
                bookmark_data.get('created_at', datetime.now().isoformat())
            ))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user_bookmarks(self, user_id: str) -> List[Dict[str, Any]]:
        """Get bookmarks for a user."""
        rows = self.connection.fetchall(
            "SELECT * FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        bookmarks = []
        for row in rows:
            bookmark = dict(row)
            bookmark['tags'] = json.loads(bookmark.get('tags', '[]'))
            bookmarks.append(bookmark)
        return bookmarks
    
    def delete_bookmark(self, bookmark_id: str) -> bool:
        """Delete a bookmark."""
        cursor = self.connection.execute(
            "DELETE FROM bookmarks WHERE bookmark_id = ?",
            (bookmark_id,)
        )
        return cursor.rowcount > 0
    
    # Favorite operations
    def add_favorite(self, favorite_data: Dict[str, Any]) -> bool:
        """Add a favorite."""
        try:
            self.connection.execute("""
                INSERT INTO favorites 
                (favorite_id, user_id, content_id, content_title, content_type, rating, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                favorite_data['favorite_id'],
                favorite_data['user_id'],
                favorite_data['content_id'],
                favorite_data['content_title'],
                favorite_data.get('content_type', 'book'),
                favorite_data.get('rating', 0),
                favorite_data.get('added_at', datetime.now().isoformat())
            ))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user_favorites(self, user_id: str) -> List[Dict[str, Any]]:
        """Get favorites for a user."""
        rows = self.connection.fetchall(
            "SELECT * FROM favorites WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,)
        )
        return [dict(row) for row in rows]
    
    def delete_favorite(self, favorite_id: str) -> bool:
        """Delete a favorite."""
        cursor = self.connection.execute(
            "DELETE FROM favorites WHERE favorite_id = ?",
            (favorite_id,)
        )
        return cursor.rowcount > 0
    
    # Notification operations
    def add_notification(self, notification_data: Dict[str, Any]) -> bool:
        """Add a notification."""
        try:
            metadata_json = json.dumps(notification_data.get('metadata', {}))
            self.connection.execute("""
                INSERT INTO notifications 
                (notification_id, user_id, title, message, type, created_at, read, action_url, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                notification_data['notification_id'],
                notification_data['user_id'],
                notification_data['title'],
                notification_data['message'],
                notification_data.get('type', 'info'),
                notification_data.get('created_at', datetime.now().isoformat()),
                1 if notification_data.get('read', False) else 0,
                notification_data.get('action_url'),
                metadata_json
            ))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False, limit: int = 50) -> List[Dict[str, Any]]:
        """Get notifications for a user."""
        query = "SELECT * FROM notifications WHERE user_id = ?"
        params = [user_id]
        
        if unread_only:
            query += " AND read = 0"
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        rows = self.connection.fetchall(query, tuple(params))
        notifications = []
        for row in rows:
            notification = dict(row)
            notification['read'] = bool(notification.get('read', 0))
            notification['metadata'] = json.loads(notification.get('metadata', '{}'))
            notifications.append(notification)
        return notifications
    
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark a notification as read."""
        cursor = self.connection.execute(
            "UPDATE notifications SET read = 1 WHERE notification_id = ?",
            (notification_id,)
        )
        return cursor.rowcount > 0


# Global instance
_database_manager: Optional[DatabaseManager] = None


def get_database_manager(db_path: str = "data/ai_reader.db") -> DatabaseManager:
    """Get the global database manager instance."""
    global _database_manager
    if _database_manager is None:
        _database_manager = DatabaseManager(db_path)
        _database_manager.initialize()
    return _database_manager
