import { useEffect } from 'react';
import './Sidebar.css';

const translations = {
  'zh-tw': {
    menu: '選單',
    home: '首頁',
    readingHistory: '閱讀歷史',
    favorites: '我的收藏',
    social: '社群互動',
    notifications: '通知中心',
    settings: '設定',
    login: '登入',
    logout: '登出',
    welcome: '歡迎',
    guest: '訪客'
  },
  'zh-cn': {
    menu: '菜单',
    home: '首页',
    readingHistory: '阅读历史',
    favorites: '我的收藏',
    social: '社区互动',
    notifications: '通知中心',
    settings: '设置',
    login: '登录',
    logout: '退出',
    welcome: '欢迎',
    guest: '访客'
  },
  'en': {
    menu: 'Menu',
    home: 'Home',
    readingHistory: 'Reading History',
    favorites: 'My Favorites',
    social: 'Social',
    notifications: 'Notifications',
    settings: 'Settings',
    login: 'Login',
    logout: 'Logout',
    welcome: 'Welcome',
    guest: 'Guest'
  },
  'ja': {
    menu: 'メニュー',
    home: 'ホーム',
    readingHistory: '閲覧履歴',
    favorites: 'お気に入り',
    social: 'コミュニティ',
    notifications: '通知',
    settings: '設定',
    login: 'ログイン',
    logout: 'ログアウト',
    welcome: 'ようこそ',
    guest: 'ゲスト'
  }
};

function Sidebar({ isOpen, onClose, onNavigate, currentUser, language = 'zh-tw' }) {
  const tr = translations[language] || translations['zh-tw'];

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const menuItems = [
    { id: 'home', icon: '🏠', label: tr.home },
    { id: 'history', icon: '📚', label: tr.readingHistory },
    { id: 'favorites', icon: '❤️', label: tr.favorites },
    { id: 'social', icon: '💬', label: tr.social },
    { id: 'notifications', icon: '🔔', label: tr.notifications },
    { id: 'settings', icon: '⚙️', label: tr.settings },
  ];

  return (
    <div className="sidebar-overlay" onClick={onClose}>
      <nav 
        className="sidebar" 
        onClick={(e) => e.stopPropagation()}
        role="navigation"
        aria-label={tr.menu}
      >
        <div className="sidebar-header">
          <div className="user-avatar">
            {currentUser ? '👤' : '👻'}
          </div>
          <div className="user-info">
            <span className="welcome-text">{tr.welcome}</span>
            <span className="user-name">
              {currentUser?.username || tr.guest}
            </span>
          </div>
          <button className="close-sidebar" onClick={onClose}>✕</button>
        </div>

        <div className="sidebar-menu">
          {menuItems.map(item => (
            <button
              key={item.id}
              className="menu-item"
              onClick={() => onNavigate(item.id)}
            >
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-label">{item.label}</span>
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          {currentUser ? (
            <button 
              className="menu-item logout-item"
              onClick={() => onNavigate('logout')}
            >
              <span className="menu-icon">🚪</span>
              <span className="menu-label">{tr.logout}</span>
            </button>
          ) : (
            <button 
              className="menu-item login-item"
              onClick={() => onNavigate('login')}
            >
              <span className="menu-icon">🔐</span>
              <span className="menu-label">{tr.login}</span>
            </button>
          )}
        </div>
      </nav>
    </div>
  );
}

export default Sidebar;
