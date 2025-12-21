"""
Bookmarks Module

Provides bookmark/favorites functionality for users.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class Bookmark:
    """
    Represents a bookmark.
    
    Attributes:
        bookmark_id: Unique bookmark identifier
        content_id: ID of the bookmarked content
        content_title: Title of the bookmarked content
        position: Position/page in the content
        note: User's note for this bookmark
        created_at: When the bookmark was created
        tags: List of tags for organization
    """
    bookmark_id: str
    content_id: str
    content_title: str
    position: str = ""
    note: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bookmark':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Favorite:
    """
    Represents a favorite item.
    
    Attributes:
        favorite_id: Unique favorite identifier
        content_id: ID of the favorite content
        content_title: Title of the content
        content_type: Type of content (book, article, etc.)
        added_at: When added to favorites
        rating: User rating (1-5)
    """
    favorite_id: str
    content_id: str
    content_title: str
    content_type: str = "book"
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    rating: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Favorite':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class UserBookmarks:
    """
    User's bookmarks and favorites collection.
    
    Attributes:
        user_id: User identifier
        bookmarks: List of bookmarks
        favorites: List of favorites
    """
    user_id: str
    bookmarks: List[Bookmark] = field(default_factory=list)
    favorites: List[Favorite] = field(default_factory=list)
    
    def add_bookmark(self, bookmark: Bookmark) -> None:
        """Add a bookmark."""
        self.bookmarks.append(bookmark)
    
    def remove_bookmark(self, bookmark_id: str) -> bool:
        """Remove a bookmark by ID."""
        for i, b in enumerate(self.bookmarks):
            if b.bookmark_id == bookmark_id:
                self.bookmarks.pop(i)
                return True
        return False
    
    def add_favorite(self, favorite: Favorite) -> None:
        """Add to favorites."""
        self.favorites.append(favorite)
    
    def remove_favorite(self, favorite_id: str) -> bool:
        """Remove from favorites by ID."""
        for i, f in enumerate(self.favorites):
            if f.favorite_id == favorite_id:
                self.favorites.pop(i)
                return True
        return False
    
    def get_bookmarks_by_content(self, content_id: str) -> List[Bookmark]:
        """Get all bookmarks for a specific content."""
        return [b for b in self.bookmarks if b.content_id == content_id]
    
    def is_favorite(self, content_id: str) -> bool:
        """Check if content is in favorites."""
        return any(f.content_id == content_id for f in self.favorites)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'bookmarks': [b.to_dict() for b in self.bookmarks],
            'favorites': [f.to_dict() for f in self.favorites]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserBookmarks':
        """Create from dictionary."""
        bookmarks = [
            Bookmark.from_dict(b) 
            for b in data.get('bookmarks', [])
        ]
        favorites = [
            Favorite.from_dict(f) 
            for f in data.get('favorites', [])
        ]
        return cls(
            user_id=data['user_id'],
            bookmarks=bookmarks,
            favorites=favorites
        )


class BookmarksManager:
    """Manages bookmarks and favorites for users."""
    
    def __init__(self):
        self._user_bookmarks: Dict[str, UserBookmarks] = {}
    
    def get_user_bookmarks(self, user_id: str) -> UserBookmarks:
        """Get or create bookmarks for a user."""
        if user_id not in self._user_bookmarks:
            self._user_bookmarks[user_id] = UserBookmarks(user_id=user_id)
        return self._user_bookmarks[user_id]
    
    def add_bookmark(self, user_id: str, bookmark: Bookmark) -> UserBookmarks:
        """Add a bookmark for a user."""
        user_bookmarks = self.get_user_bookmarks(user_id)
        user_bookmarks.add_bookmark(bookmark)
        return user_bookmarks
    
    def remove_bookmark(self, user_id: str, bookmark_id: str) -> bool:
        """Remove a bookmark for a user."""
        user_bookmarks = self.get_user_bookmarks(user_id)
        return user_bookmarks.remove_bookmark(bookmark_id)
    
    def add_favorite(self, user_id: str, favorite: Favorite) -> UserBookmarks:
        """Add a favorite for a user."""
        user_bookmarks = self.get_user_bookmarks(user_id)
        user_bookmarks.add_favorite(favorite)
        return user_bookmarks
    
    def remove_favorite(self, user_id: str, favorite_id: str) -> bool:
        """Remove a favorite for a user."""
        user_bookmarks = self.get_user_bookmarks(user_id)
        return user_bookmarks.remove_favorite(favorite_id)


# Global instance
_bookmarks_manager: Optional[BookmarksManager] = None


def get_bookmarks_manager() -> BookmarksManager:
    """Get the global bookmarks manager instance."""
    global _bookmarks_manager
    if _bookmarks_manager is None:
        _bookmarks_manager = BookmarksManager()
    return _bookmarks_manager
