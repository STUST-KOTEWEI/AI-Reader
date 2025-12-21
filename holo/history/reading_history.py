"""
Reading History Module

Provides reading history tracking for users.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json


@dataclass
class ReadingSession:
    """
    Represents a single reading session.
    
    Attributes:
        session_id: Unique session identifier
        content_id: ID of the content being read
        content_title: Title of the content
        started_at: When the session started
        ended_at: When the session ended
        progress: Reading progress percentage (0-100)
        duration_seconds: Total duration in seconds
    """
    session_id: str
    content_id: str
    content_title: str
    started_at: str
    ended_at: Optional[str] = None
    progress: float = 0.0
    duration_seconds: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReadingSession':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ReadingHistory:
    """
    User's reading history.
    
    Attributes:
        user_id: User identifier
        sessions: List of reading sessions
        total_reading_time: Total reading time in seconds
        books_completed: Number of books completed
    """
    user_id: str
    sessions: List[ReadingSession] = field(default_factory=list)
    total_reading_time: int = 0
    books_completed: int = 0
    
    def add_session(self, session: ReadingSession) -> None:
        """Add a reading session."""
        self.sessions.append(session)
        self.total_reading_time += session.duration_seconds
        if session.progress >= 100:
            self.books_completed += 1
    
    def get_recent_sessions(self, limit: int = 10) -> List[ReadingSession]:
        """Get recent reading sessions."""
        sorted_sessions = sorted(
            self.sessions,
            key=lambda s: s.started_at,
            reverse=True
        )
        return sorted_sessions[:limit]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'sessions': [s.to_dict() for s in self.sessions],
            'total_reading_time': self.total_reading_time,
            'books_completed': self.books_completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReadingHistory':
        """Create from dictionary."""
        sessions = [
            ReadingSession.from_dict(s) 
            for s in data.get('sessions', [])
        ]
        return cls(
            user_id=data['user_id'],
            sessions=sessions,
            total_reading_time=data.get('total_reading_time', 0),
            books_completed=data.get('books_completed', 0)
        )


class HistoryManager:
    """Manages reading history for users."""
    
    def __init__(self):
        self._histories: Dict[str, ReadingHistory] = {}
    
    def get_history(self, user_id: str) -> ReadingHistory:
        """Get or create reading history for a user."""
        if user_id not in self._histories:
            self._histories[user_id] = ReadingHistory(user_id=user_id)
        return self._histories[user_id]
    
    def add_session(self, user_id: str, session: ReadingSession) -> ReadingHistory:
        """Add a reading session for a user."""
        history = self.get_history(user_id)
        history.add_session(session)
        return history
    
    def clear_history(self, user_id: str) -> bool:
        """Clear reading history for a user."""
        if user_id in self._histories:
            self._histories[user_id] = ReadingHistory(user_id=user_id)
            return True
        return False


# Global instance
_history_manager: Optional[HistoryManager] = None


def get_history_manager() -> HistoryManager:
    """Get the global history manager instance."""
    global _history_manager
    if _history_manager is None:
        _history_manager = HistoryManager()
    return _history_manager
