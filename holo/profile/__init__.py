"""
User Profile Module

Provides user profile management for personalized immersive experiences.
"""

from .user_profile import (
    UserProfile,
    UserPreferences,
    AccessibilitySettings,
    DEFAULT_USER_ID,
    DEFAULT_DISPLAY_NAME
)

__all__ = [
    'UserProfile',
    'UserPreferences',
    'AccessibilitySettings',
    'DEFAULT_USER_ID',
    'DEFAULT_DISPLAY_NAME'
]
