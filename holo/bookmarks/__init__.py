"""
Bookmarks Module

Provides bookmark and favorites functionality for users.
"""

from .bookmarks import (
    Bookmark,
    Favorite,
    UserBookmarks,
    BookmarksManager,
    get_bookmarks_manager
)

__all__ = [
    'Bookmark',
    'Favorite',
    'UserBookmarks',
    'BookmarksManager',
    'get_bookmarks_manager'
]
