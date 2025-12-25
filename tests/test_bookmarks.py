"""
Tests for Bookmarks Module
"""

import pytest
from holo.bookmarks import (
    Bookmark,
    Favorite,
    UserBookmarks,
    BookmarksManager,
    get_bookmarks_manager
)


class TestBookmark:
    """Tests for Bookmark dataclass."""
    
    def test_create_bookmark(self):
        """Test creating a bookmark."""
        bookmark = Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Test Book"
        )
        assert bookmark.bookmark_id == "bm_001"
        assert bookmark.content_id == "book_001"
        assert bookmark.note == ""
    
    def test_bookmark_with_note(self):
        """Test bookmark with note."""
        bookmark = Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Test Book",
            position="Chapter 3, Page 45",
            note="Important quote",
            tags=["important", "quote"]
        )
        assert bookmark.note == "Important quote"
        assert len(bookmark.tags) == 2
    
    def test_bookmark_to_dict(self):
        """Test converting bookmark to dictionary."""
        bookmark = Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Test Book",
            note="Test note"
        )
        data = bookmark.to_dict()
        assert data['bookmark_id'] == "bm_001"
        assert data['note'] == "Test note"


class TestFavorite:
    """Tests for Favorite dataclass."""
    
    def test_create_favorite(self):
        """Test creating a favorite."""
        favorite = Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book"
        )
        assert favorite.favorite_id == "fav_001"
        assert favorite.content_type == "book"
        assert favorite.rating == 0
    
    def test_favorite_with_rating(self):
        """Test favorite with rating."""
        favorite = Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book",
            rating=5
        )
        assert favorite.rating == 5
    
    def test_favorite_to_dict(self):
        """Test converting favorite to dictionary."""
        favorite = Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book",
            content_type="article",
            rating=4
        )
        data = favorite.to_dict()
        assert data['content_type'] == "article"
        assert data['rating'] == 4


class TestUserBookmarks:
    """Tests for UserBookmarks dataclass."""
    
    def test_create_user_bookmarks(self):
        """Test creating user bookmarks."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        assert user_bookmarks.user_id == "user_001"
        assert len(user_bookmarks.bookmarks) == 0
        assert len(user_bookmarks.favorites) == 0
    
    def test_add_bookmark(self):
        """Test adding a bookmark."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        bookmark = Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Test Book"
        )
        user_bookmarks.add_bookmark(bookmark)
        assert len(user_bookmarks.bookmarks) == 1
    
    def test_remove_bookmark(self):
        """Test removing a bookmark."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        bookmark = Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Test Book"
        )
        user_bookmarks.add_bookmark(bookmark)
        
        result = user_bookmarks.remove_bookmark("bm_001")
        assert result is True
        assert len(user_bookmarks.bookmarks) == 0
    
    def test_add_favorite(self):
        """Test adding a favorite."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        favorite = Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book"
        )
        user_bookmarks.add_favorite(favorite)
        assert len(user_bookmarks.favorites) == 1
    
    def test_remove_favorite(self):
        """Test removing a favorite."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        favorite = Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book"
        )
        user_bookmarks.add_favorite(favorite)
        
        result = user_bookmarks.remove_favorite("fav_001")
        assert result is True
        assert len(user_bookmarks.favorites) == 0
    
    def test_get_bookmarks_by_content(self):
        """Test getting bookmarks by content."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        user_bookmarks.add_bookmark(Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Book 1"
        ))
        user_bookmarks.add_bookmark(Bookmark(
            bookmark_id="bm_002",
            content_id="book_001",
            content_title="Book 1"
        ))
        user_bookmarks.add_bookmark(Bookmark(
            bookmark_id="bm_003",
            content_id="book_002",
            content_title="Book 2"
        ))
        
        bookmarks = user_bookmarks.get_bookmarks_by_content("book_001")
        assert len(bookmarks) == 2
    
    def test_is_favorite(self):
        """Test checking if content is favorite."""
        user_bookmarks = UserBookmarks(user_id="user_001")
        user_bookmarks.add_favorite(Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book"
        ))
        
        assert user_bookmarks.is_favorite("book_001") is True
        assert user_bookmarks.is_favorite("book_002") is False


class TestBookmarksManager:
    """Tests for BookmarksManager."""
    
    def test_get_user_bookmarks(self):
        """Test getting user bookmarks."""
        manager = BookmarksManager()
        user_bookmarks = manager.get_user_bookmarks("user_001")
        assert user_bookmarks.user_id == "user_001"
    
    def test_add_bookmark_via_manager(self):
        """Test adding bookmark via manager."""
        manager = BookmarksManager()
        bookmark = Bookmark(
            bookmark_id="bm_001",
            content_id="book_001",
            content_title="Test Book"
        )
        user_bookmarks = manager.add_bookmark("user_001", bookmark)
        assert len(user_bookmarks.bookmarks) == 1
    
    def test_add_favorite_via_manager(self):
        """Test adding favorite via manager."""
        manager = BookmarksManager()
        favorite = Favorite(
            favorite_id="fav_001",
            content_id="book_001",
            content_title="Test Book"
        )
        user_bookmarks = manager.add_favorite("user_001", favorite)
        assert len(user_bookmarks.favorites) == 1


class TestGetBookmarksManager:
    """Tests for global bookmarks manager."""
    
    def test_get_global_manager(self):
        """Test getting global bookmarks manager."""
        manager = get_bookmarks_manager()
        assert manager is not None
        assert isinstance(manager, BookmarksManager)
