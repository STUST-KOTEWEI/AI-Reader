"""
Social Features Module

Provides social functionality including sharing and comments.
"""

from .social import (
    Comment,
    Share,
    ContentStats,
    SocialManager,
    get_social_manager
)

__all__ = [
    'Comment',
    'Share',
    'ContentStats',
    'SocialManager',
    'get_social_manager'
]
