"""
Notification System Module

Provides notification functionality for users.
"""

from .notification_manager import (
    NotificationType,
    Notification,
    NotificationPreferences,
    NotificationManager,
    get_notification_manager
)

__all__ = [
    'NotificationType',
    'Notification',
    'NotificationPreferences',
    'NotificationManager',
    'get_notification_manager'
]
