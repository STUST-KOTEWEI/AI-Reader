import { useState, useEffect } from 'react';
import './NotificationsPanel.css';

const API_URL = 'http://127.0.0.1:8000';

const translations = {
  'zh-tw': {
    title: '通知中心',
    noNotifications: '暫無通知',
    markAllRead: '全部標為已讀',
    clearAll: '清除全部',
    refresh: '重新整理',
    justNow: '剛剛',
    minutesAgo: '分鐘前',
    hoursAgo: '小時前',
    daysAgo: '天前',
    types: {
      info: '資訊',
      success: '成功',
      warning: '警告',
      error: '錯誤',
      comment: '評論',
      share: '分享',
      recommendation: '推薦'
    }
  },
  'zh-cn': {
    title: '通知中心',
    noNotifications: '暂无通知',
    markAllRead: '全部标为已读',
    clearAll: '清除全部',
    refresh: '刷新',
    justNow: '刚刚',
    minutesAgo: '分钟前',
    hoursAgo: '小时前',
    daysAgo: '天前',
    types: {
      info: '信息',
      success: '成功',
      warning: '警告',
      error: '错误',
      comment: '评论',
      share: '分享',
      recommendation: '推荐'
    }
  },
  'en': {
    title: 'Notifications',
    noNotifications: 'No notifications',
    markAllRead: 'Mark all as read',
    clearAll: 'Clear all',
    refresh: 'Refresh',
    justNow: 'Just now',
    minutesAgo: 'minutes ago',
    hoursAgo: 'hours ago',
    daysAgo: 'days ago',
    types: {
      info: 'Info',
      success: 'Success',
      warning: 'Warning',
      error: 'Error',
      comment: 'Comment',
      share: 'Share',
      recommendation: 'Recommendation'
    }
  },
  'ja': {
    title: '通知',
    noNotifications: '通知はありません',
    markAllRead: 'すべて既読にする',
    clearAll: 'すべて削除',
    refresh: '更新',
    justNow: 'たった今',
    minutesAgo: '分前',
    hoursAgo: '時間前',
    daysAgo: '日前',
    types: {
      info: 'お知らせ',
      success: '成功',
      warning: '警告',
      error: 'エラー',
      comment: 'コメント',
      share: '共有',
      recommendation: 'おすすめ'
    }
  }
};

function NotificationsPanel({ isOpen, onClose, notifications = [], onRefresh, language = 'zh-tw', userId }) {
  const tr = translations[language] || translations['zh-tw'];
  const [localNotifications, setLocalNotifications] = useState(notifications);

  useEffect(() => {
    setLocalNotifications(notifications);
  }, [notifications]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    
    if (diff < 60) return tr.justNow;
    if (diff < 3600) return `${Math.floor(diff / 60)} ${tr.minutesAgo}`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} ${tr.hoursAgo}`;
    return `${Math.floor(diff / 86400)} ${tr.daysAgo}`;
  };

  const getTypeIcon = (type) => {
    const icons = {
      info: 'ℹ️',
      success: '✅',
      warning: '⚠️',
      error: '❌',
      comment: '💬',
      share: '📤',
      recommendation: '⭐'
    };
    return icons[type] || 'ℹ️';
  };

  const markAsRead = async (notificationId) => {
    if (!userId) return;
    try {
      await fetch(`${API_URL}/notifications/${userId}/${notificationId}/read`, {
        method: 'PUT'
      });
      setLocalNotifications(prev => 
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      );
    } catch (err) {
      console.error('Failed to mark as read:', err);
    }
  };

  const markAllAsRead = async () => {
    if (!userId) return;
    try {
      // Mark all as read locally
      setLocalNotifications(prev => prev.map(n => ({ ...n, read: true })));
      // In a real app, you'd have an API endpoint for this
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error('Failed to mark all as read:', err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="notifications-overlay" onClick={onClose}>
      <div 
        className="notifications-panel" 
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-label={tr.title}
      >
        <header className="notifications-header">
          <h2>{tr.title}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </header>

        <div className="notifications-actions">
          <button className="action-btn" onClick={onRefresh}>
            🔄 {tr.refresh}
          </button>
          <button className="action-btn" onClick={markAllAsRead}>
            ✓ {tr.markAllRead}
          </button>
        </div>

        <div className="notifications-list">
          {localNotifications.length === 0 ? (
            <div className="empty-state">
              <span className="empty-icon">🔔</span>
              <p>{tr.noNotifications}</p>
            </div>
          ) : (
            localNotifications.map(notification => (
              <div 
                key={notification.id}
                className={`notification-item ${notification.read ? 'read' : 'unread'}`}
                onClick={() => markAsRead(notification.id)}
              >
                <div className="notification-icon">
                  {getTypeIcon(notification.type)}
                </div>
                <div className="notification-content">
                  <h4>{notification.title}</h4>
                  <p>{notification.message}</p>
                  <span className="notification-time">
                    {formatTime(notification.created_at)}
                  </span>
                </div>
                {!notification.read && (
                  <div className="unread-indicator" />
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default NotificationsPanel;
