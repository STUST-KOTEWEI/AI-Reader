"""
Notification System Module

Provides notification functionality for users.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum


class NotificationType(Enum):
    """Types of notifications."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SOCIAL = "social"
    SYSTEM = "system"
    RECOMMENDATION = "recommendation"


@dataclass
class Notification:
    """
    Represents a notification.
    
    Attributes:
        notification_id: Unique notification identifier
        user_id: Target user ID
        title: Notification title
        message: Notification message
        type: Notification type
        created_at: When notification was created
        read: Whether notification has been read
        action_url: Optional URL for notification action
        metadata: Additional notification data
    """
    notification_id: str
    user_id: str
    title: str
    message: str
    type: str = NotificationType.INFO.value
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    read: bool = False
    action_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Notification':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class NotificationPreferences:
    """
    User's notification preferences.
    
    Attributes:
        user_id: User identifier
        email_enabled: Enable email notifications
        push_enabled: Enable push notifications
        in_app_enabled: Enable in-app notifications
        social_notifications: Enable social notifications
        recommendation_notifications: Enable recommendation notifications
        system_notifications: Enable system notifications
        quiet_hours_start: Start of quiet hours (HH:MM)
        quiet_hours_end: End of quiet hours (HH:MM)
    """
    user_id: str
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    social_notifications: bool = True
    recommendation_notifications: bool = True
    system_notifications: bool = True
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class NotificationManager:
    """Manages user notifications."""
    
    def __init__(self):
        self._notifications: Dict[str, List[Notification]] = {}  # user_id -> notifications
        self._preferences: Dict[str, NotificationPreferences] = {}
    
    def send_notification(
        self,
        notification_id: str,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = NotificationType.INFO.value,
        action_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Notification]:
        """Send a notification to a user."""
        # Check preferences
        prefs = self._preferences.get(user_id)
        if prefs:
            if notification_type == NotificationType.SOCIAL.value and not prefs.social_notifications:
                return None
            if notification_type == NotificationType.RECOMMENDATION.value and not prefs.recommendation_notifications:
                return None
            if notification_type == NotificationType.SYSTEM.value and not prefs.system_notifications:
                return None
            if not prefs.in_app_enabled:
                return None
        
        notification = Notification(
            notification_id=notification_id,
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            action_url=action_url,
            metadata=metadata or {}
        )
        
        if user_id not in self._notifications:
            self._notifications[user_id] = []
        self._notifications[user_id].append(notification)
        
        return notification
    
    def get_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user."""
        notifications = self._notifications.get(user_id, [])
        
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        
        # Sort by created_at, newest first
        notifications.sort(key=lambda n: n.created_at, reverse=True)
        
        return notifications[:limit]
    
    def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications."""
        notifications = self._notifications.get(user_id, [])
        return sum(1 for n in notifications if not n.read)
    
    def mark_as_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read."""
        for notification in self._notifications.get(user_id, []):
            if notification.notification_id == notification_id:
                notification.read = True
                return True
        return False
    
    def mark_all_as_read(self, user_id: str) -> int:
        """Mark all notifications as read. Returns count of marked notifications."""
        count = 0
        for notification in self._notifications.get(user_id, []):
            if not notification.read:
                notification.read = True
                count += 1
        return count
    
    def delete_notification(self, user_id: str, notification_id: str) -> bool:
        """Delete a notification."""
        if user_id not in self._notifications:
            return False
        
        for i, notification in enumerate(self._notifications[user_id]):
            if notification.notification_id == notification_id:
                self._notifications[user_id].pop(i)
                return True
        return False
    
    def clear_notifications(self, user_id: str) -> int:
        """Clear all notifications for a user. Returns count of cleared notifications."""
        if user_id in self._notifications:
            count = len(self._notifications[user_id])
            self._notifications[user_id] = []
            return count
        return 0
    
    def set_preferences(self, preferences: NotificationPreferences) -> None:
        """Set notification preferences for a user."""
        self._preferences[preferences.user_id] = preferences
    
    def get_preferences(self, user_id: str) -> NotificationPreferences:
        """Get notification preferences for a user."""
        if user_id not in self._preferences:
            self._preferences[user_id] = NotificationPreferences(user_id=user_id)
        return self._preferences[user_id]
    
    # Convenience methods for common notifications
    def notify_new_comment(
        self,
        notification_id: str,
        user_id: str,
        commenter_name: str,
        content_title: str,
        content_id: str
    ) -> Optional[Notification]:
        """Send notification for a new comment."""
        return self.send_notification(
            notification_id=notification_id,
            user_id=user_id,
            title="新留言",
            message=f"{commenter_name} 在 {content_title} 留言了",
            notification_type=NotificationType.SOCIAL.value,
            action_url=f"/content/{content_id}",
            metadata={"content_id": content_id, "commenter": commenter_name}
        )
    
    def notify_new_recommendation(
        self,
        notification_id: str,
        user_id: str,
        content_title: str,
        content_id: str
    ) -> Optional[Notification]:
        """Send notification for a new recommendation."""
        return self.send_notification(
            notification_id=notification_id,
            user_id=user_id,
            title="推薦內容",
            message=f"為您推薦: {content_title}",
            notification_type=NotificationType.RECOMMENDATION.value,
            action_url=f"/content/{content_id}",
            metadata={"content_id": content_id}
        )
    
    def notify_reading_goal(
        self,
        notification_id: str,
        user_id: str,
        goal_type: str,
        progress: int
    ) -> Optional[Notification]:
        """Send notification for reading goal progress."""
        return self.send_notification(
            notification_id=notification_id,
            user_id=user_id,
            title="閱讀目標",
            message=f"您的{goal_type}目標已完成 {progress}%!",
            notification_type=NotificationType.SUCCESS.value,
            metadata={"goal_type": goal_type, "progress": progress}
        )


# Global instance
_notification_manager: Optional[NotificationManager] = None


def get_notification_manager() -> NotificationManager:
    """Get the global notification manager instance."""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager
