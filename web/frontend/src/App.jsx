import { useState, useEffect, useCallback } from 'react';
import './App.css';
import UserProfile from './components/UserProfile';
import ReadingProgress from './components/ReadingProgress';
import FavoritesList from './components/FavoritesList';
import LoginPage from './components/LoginPage';
import NotificationsPanel from './components/NotificationsPanel';
import SocialPanel from './components/SocialPanel';
import Sidebar from './components/Sidebar';
import { ThemeProvider, useTheme } from './contexts/ThemeContext';
import { t } from './i18n/translations';

// 後端 API 的網址
const API_URL = 'http://127.0.0.1:8000';

function AppContent() {
  const { theme, themeName, toggleTheme } = useTheme();
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [audioSrc, setAudioSrc] = useState('');
  const [ttsLoading, setTtsLoading] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [progressOpen, setProgressOpen] = useState(false);
  const [favoritesOpen, setFavoritesOpen] = useState(false);
  const [loginOpen, setLoginOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [socialOpen, setSocialOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [language, setLanguage] = useState('zh-tw');
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  // Load user from localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
      try {
        setCurrentUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('currentUser');
      }
    }
  }, []);

  // Fetch notifications when user is logged in
  const fetchNotifications = useCallback(async () => {
    if (!currentUser?.user_id) return;
    try {
      const response = await fetch(`${API_URL}/notifications/${currentUser.user_id}`);
      if (response.ok) {
        const data = await response.json();
        setNotifications(data.notifications || []);
        setUnreadCount(data.notifications?.filter(n => !n.read).length || 0);
      }
    } catch (err) {
      console.error('Failed to fetch notifications:', err);
    }
  }, [currentUser?.user_id]);

  useEffect(() => {
    fetchNotifications();
    // Poll for new notifications every 30 seconds
    const interval = setInterval(fetchNotifications, 30000);
    return () => clearInterval(interval);
  }, [fetchNotifications]);

  const handleLogin = (userData) => {
    setCurrentUser(userData);
    localStorage.setItem('currentUser', JSON.stringify(userData));
    fetchNotifications();
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('currentUser');
    setNotifications([]);
    setUnreadCount(0);
  };

  const handleProfileChange = (profile) => {
    setUserProfile(profile);
    // Update language when profile changes
    if (profile?.preferences?.preferred_language) {
      setLanguage(profile.preferences.preferred_language);
    }
  };

  const handleTTS = async () => {
    if (!text.trim()) {
      setError(t(language, 'placeholder'));
      return;
    }
    setTtsLoading(true);
    setError('');
    setAudioSrc('');

    try {
        const response = await fetch(`${API_URL}/tts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, lang: language })
        });

        if (!response.ok) {
            throw new Error(`TTS API error: ${response.status}`);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setAudioSrc(url);
    } catch (err) {
        setError(err.message);
    } finally {
        setTtsLoading(false);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    if (!text.trim()) {
      setError(t(language, 'placeholder'));
      setLoading(false);
      return;
    }

    try {
      const requestBody = { text: text };
      // Include user profile in request if available
      if (userProfile) {
        requestBody.user_profile = userProfile;
      }
      
      const response = await fetch(`${API_URL}/generate_immersion`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle adding to favorites
  const handleAddToFavorites = async () => {
    if (!currentUser?.user_id || !result) return;
    try {
      await fetch(`${API_URL}/bookmarks/${currentUser.user_id}/favorite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content_id: `content_${Date.now()}`,
          content_type: 'immersion',
          title: text.slice(0, 50),
          description: text
        })
      });
    } catch (err) {
      console.error('Failed to add to favorites:', err);
    }
  };

  // Save reading session
  const saveReadingSession = async () => {
    if (!currentUser?.user_id) return;
    try {
      await fetch(`${API_URL}/history/${currentUser.user_id}/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content_id: `content_${Date.now()}`,
          content_type: 'immersion',
          progress: 100,
          duration_seconds: 60
        })
      });
    } catch (err) {
      console.error('Failed to save reading session:', err);
    }
  };

  return (
    <div className={`App ${themeName}`} data-theme={themeName}>
      {/* Sidebar Navigation */}
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNavigate={(section) => {
          setSidebarOpen(false);
          switch (section) {
            case 'history': setProgressOpen(true); break;
            case 'favorites': setFavoritesOpen(true); break;
            case 'settings': setProfileOpen(true); break;
            case 'social': setSocialOpen(true); break;
            case 'notifications': setNotificationsOpen(true); break;
            case 'login': setLoginOpen(true); break;
            case 'logout': handleLogout(); break;
            default: break;
          }
        }}
        currentUser={currentUser}
        language={language}
      />

      <header className="App-header">
        <div className="header-left">
          <button 
            className="menu-button" 
            onClick={() => setSidebarOpen(true)}
            aria-label={t(language, 'menu')}
          >
            ☰
          </button>
        </div>

        <div className="header-center">
          <h1>{t(language, 'appTitle')}</h1>
          <p>{t(language, 'appSubtitle')}</p>
        </div>

        <div className="header-buttons">
          {/* Theme Toggle */}
          <button 
            className="header-button theme-toggle" 
            onClick={toggleTheme}
            aria-label={t(language, 'theme')}
            title={`${t(language, 'theme')}: ${themeName}`}
          >
            {themeName === 'dark' ? '🌙' : themeName === 'light' ? '☀️' : '🔄'}
          </button>

          {/* Notifications */}
          <button 
            className="header-button notification-button" 
            onClick={() => setNotificationsOpen(true)}
            aria-label={t(language, 'notifications')}
          >
            🔔
            {unreadCount > 0 && (
              <span className="notification-badge">{unreadCount}</span>
            )}
          </button>

          {/* Quick Actions */}
          <button 
            className="header-button" 
            onClick={() => setProgressOpen(true)}
            aria-label={t(language, 'readingHistory')}
          >
            📊
          </button>
          <button 
            className="header-button" 
            onClick={() => setFavoritesOpen(true)}
            aria-label={t(language, 'favorites')}
          >
            ❤️
          </button>
          <button 
            className="header-button" 
            onClick={() => setSocialOpen(true)}
            aria-label={t(language, 'social')}
          >
            💬
          </button>

          {/* User/Login Button */}
          {currentUser ? (
            <button 
              className="profile-button user-logged-in" 
              onClick={() => setProfileOpen(true)}
              aria-label={t(language, 'settings')}
            >
              👤 {currentUser.username || t(language, 'settings')}
            </button>
          ) : (
            <button 
              className="profile-button login-button" 
              onClick={() => setLoginOpen(true)}
              aria-label={t(language, 'login')}
            >
              🔐 {t(language, 'login')}
            </button>
          )}
        </div>
      </header>

      <main>
        <form onSubmit={handleSubmit} className="narrative-form">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={t(language, 'placeholder')}
            rows="5"
            disabled={loading}
          />
          <div className="form-buttons">
            <button type="submit" className="primary-button" disabled={loading}>
              {loading ? t(language, 'generating') : t(language, 'generate')}
            </button>
            <button type="button" className="secondary-button" onClick={handleTTS} disabled={ttsLoading}>
              {ttsLoading ? t(language, 'generatingAudio') : t(language, 'playAudio')}
            </button>
          </div>
        </form>

        {error && <p className="error-message">{error}</p>}

        {audioSrc && (
          <div className="audio-player">
            <h3>{t(language, 'audioOutput')}</h3>
            <audio controls autoPlay src={audioSrc}>
              {t(language, 'browserNotSupported')}
            </audio>
          </div>
        )}

        {result && (
          <div className="result-container">
            <div className="result-header">
              <h2>{t(language, 'results')}</h2>
              <div className="result-actions">
                <button 
                  className="action-button" 
                  onClick={handleAddToFavorites}
                  disabled={!currentUser}
                  title={currentUser ? t(language, 'addToFavorites') : t(language, 'loginRequired')}
                >
                  ❤️ {t(language, 'addToFavorites')}
                </button>
                <button 
                  className="action-button" 
                  onClick={() => setSocialOpen(true)}
                >
                  📤 {t(language, 'share')}
                </button>
                <button 
                  className="action-button" 
                  onClick={saveReadingSession}
                  disabled={!currentUser}
                >
                  💾 {t(language, 'saveProgress')}
                </button>
              </div>
            </div>
            <div className="result-section">
              <h3>{t(language, 'auditoryOutput')}</h3>
              <pre>{JSON.stringify(result.auditory_output, null, 2)}</pre>
            </div>
            <div className="result-section">
              <h3>{t(language, 'sensoryOutput')}</h3>
              <pre>{JSON.stringify(result.sensory_output, null, 2)}</pre>
            </div>
            <div className="result-section">
              <h3>{t(language, 'knowledgeGraph')}</h3>
              <pre>{JSON.stringify(result.knowledge_graph, null, 2)}</pre>
            </div>
          </div>
        )}
      </main>

      {/* Modals/Panels */}
      <UserProfile
        isOpen={profileOpen}
        onClose={() => setProfileOpen(false)}
        onProfileChange={handleProfileChange}
        language={language}
        userId={currentUser?.user_id}
      />

      <ReadingProgress
        isOpen={progressOpen}
        onClose={() => setProgressOpen(false)}
        language={language}
        userId={currentUser?.user_id}
      />

      <FavoritesList
        isOpen={favoritesOpen}
        onClose={() => setFavoritesOpen(false)}
        language={language}
        userId={currentUser?.user_id}
      />

      <LoginPage
        isOpen={loginOpen}
        onClose={() => setLoginOpen(false)}
        onLogin={handleLogin}
        language={language}
      />

      <NotificationsPanel
        isOpen={notificationsOpen}
        onClose={() => setNotificationsOpen(false)}
        notifications={notifications}
        onRefresh={fetchNotifications}
        language={language}
        userId={currentUser?.user_id}
      />

      <SocialPanel
        isOpen={socialOpen}
        onClose={() => setSocialOpen(false)}
        language={language}
        userId={currentUser?.user_id}
        contentId={result ? `content_${Date.now()}` : null}
      />
    </div>
  );
}

// Main App component with ThemeProvider
function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
