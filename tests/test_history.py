"""
Tests for History Module
"""

import pytest
from holo.history import (
    ReadingSession,
    ReadingHistory,
    HistoryManager,
    get_history_manager
)


class TestReadingSession:
    """Tests for ReadingSession dataclass."""
    
    def test_create_session(self):
        """Test creating a reading session."""
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00"
        )
        assert session.session_id == "sess_001"
        assert session.content_id == "book_001"
        assert session.progress == 0.0
    
    def test_session_to_dict(self):
        """Test converting session to dictionary."""
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00",
            progress=50.0,
            duration_seconds=3600
        )
        data = session.to_dict()
        assert data['session_id'] == "sess_001"
        assert data['progress'] == 50.0
        assert data['duration_seconds'] == 3600
    
    def test_session_from_dict(self):
        """Test creating session from dictionary."""
        data = {
            'session_id': 'sess_002',
            'content_id': 'book_002',
            'content_title': 'Another Book',
            'started_at': '2024-01-01T12:00:00',
            'progress': 75.0
        }
        session = ReadingSession.from_dict(data)
        assert session.session_id == 'sess_002'
        assert session.progress == 75.0


class TestReadingHistory:
    """Tests for ReadingHistory dataclass."""
    
    def test_create_history(self):
        """Test creating reading history."""
        history = ReadingHistory(user_id="user_001")
        assert history.user_id == "user_001"
        assert len(history.sessions) == 0
        assert history.total_reading_time == 0
    
    def test_add_session(self):
        """Test adding a session to history."""
        history = ReadingHistory(user_id="user_001")
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00",
            duration_seconds=1800
        )
        history.add_session(session)
        assert len(history.sessions) == 1
        assert history.total_reading_time == 1800
    
    def test_add_completed_session(self):
        """Test adding a completed session."""
        history = ReadingHistory(user_id="user_001")
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00",
            progress=100.0,
            duration_seconds=7200
        )
        history.add_session(session)
        assert history.books_completed == 1
    
    def test_get_recent_sessions(self):
        """Test getting recent sessions."""
        history = ReadingHistory(user_id="user_001")
        for i in range(15):
            session = ReadingSession(
                session_id=f"sess_{i:03d}",
                content_id=f"book_{i:03d}",
                content_title=f"Book {i}",
                started_at=f"2024-01-{i+1:02d}T10:00:00"
            )
            history.add_session(session)
        
        recent = history.get_recent_sessions(10)
        assert len(recent) == 10
    
    def test_history_to_dict(self):
        """Test converting history to dictionary."""
        history = ReadingHistory(user_id="user_001")
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00"
        )
        history.add_session(session)
        
        data = history.to_dict()
        assert data['user_id'] == "user_001"
        assert len(data['sessions']) == 1


class TestHistoryManager:
    """Tests for HistoryManager."""
    
    def test_get_history(self):
        """Test getting user history."""
        manager = HistoryManager()
        history = manager.get_history("user_001")
        assert history.user_id == "user_001"
    
    def test_add_session_via_manager(self):
        """Test adding session via manager."""
        manager = HistoryManager()
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00",
            duration_seconds=1800
        )
        history = manager.add_session("user_001", session)
        assert len(history.sessions) == 1
    
    def test_clear_history(self):
        """Test clearing history."""
        manager = HistoryManager()
        session = ReadingSession(
            session_id="sess_001",
            content_id="book_001",
            content_title="Test Book",
            started_at="2024-01-01T10:00:00"
        )
        manager.add_session("user_001", session)
        
        result = manager.clear_history("user_001")
        assert result is True
        
        history = manager.get_history("user_001")
        assert len(history.sessions) == 0


class TestGetHistoryManager:
    """Tests for global history manager."""
    
    def test_get_global_manager(self):
        """Test getting global history manager."""
        manager = get_history_manager()
        assert manager is not None
        assert isinstance(manager, HistoryManager)
