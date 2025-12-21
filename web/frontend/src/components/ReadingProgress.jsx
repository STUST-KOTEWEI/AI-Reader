import { useState, useEffect } from 'react';
import './ReadingProgress.css';
import { t } from '../i18n/translations';

const API_URL = 'http://127.0.0.1:8000';

/**
 * ReadingProgress Component
 * 
 * Displays reading history and progress tracking.
 */
function ReadingProgress({ isOpen, onClose, language = 'zh-tw', userId = 'default' }) {
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  const fetchHistory = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_URL}/history/${userId}`);
      if (!response.ok) {
        throw new Error('無法載入閱讀歷史');
      }
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString(language === 'en' ? 'en-US' : 'zh-TW', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!isOpen) return null;

  const translations = {
    'zh-tw': {
      title: '閱讀歷史',
      totalTime: '總閱讀時間',
      booksCompleted: '已完成書籍',
      recentSessions: '最近閱讀',
      noHistory: '尚無閱讀記錄',
      progress: '進度',
      duration: '時長'
    },
    'en': {
      title: 'Reading History',
      totalTime: 'Total Reading Time',
      booksCompleted: 'Books Completed',
      recentSessions: 'Recent Sessions',
      noHistory: 'No reading history yet',
      progress: 'Progress',
      duration: 'Duration'
    },
    'ja': {
      title: '閲覧履歴',
      totalTime: '合計閲覧時間',
      booksCompleted: '完了した本',
      recentSessions: '最近の閲覧',
      noHistory: '閲覧履歴がありません',
      progress: '進捗',
      duration: '時間'
    },
    'zh-cn': {
      title: '阅读历史',
      totalTime: '总阅读时间',
      booksCompleted: '已完成书籍',
      recentSessions: '最近阅读',
      noHistory: '暂无阅读记录',
      progress: '进度',
      duration: '时长'
    }
  };

  const tr = translations[language] || translations['zh-tw'];

  return (
    <div className="progress-overlay" onClick={onClose}>
      <div className="progress-panel" onClick={(e) => e.stopPropagation()}>
        <div className="progress-header">
          <h2>{tr.title}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {loading && <p className="loading">載入中...</p>}
        {error && <p className="error-message">{error}</p>}

        {history && (
          <div className="progress-content">
            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-value">{formatDuration(history.total_reading_time)}</span>
                <span className="stat-label">{tr.totalTime}</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">{history.books_completed}</span>
                <span className="stat-label">{tr.booksCompleted}</span>
              </div>
            </div>

            <div className="sessions-section">
              <h3>{tr.recentSessions}</h3>
              {history.sessions.length === 0 ? (
                <p className="no-data">{tr.noHistory}</p>
              ) : (
                <div className="sessions-list">
                  {history.sessions.slice(0, 10).map((session, index) => (
                    <div key={index} className="session-item">
                      <div className="session-info">
                        <span className="session-title">{session.content_title}</span>
                        <span className="session-date">{formatDate(session.started_at)}</span>
                      </div>
                      <div className="session-stats">
                        <div className="progress-bar-container">
                          <div 
                            className="progress-bar-fill" 
                            style={{ width: `${session.progress}%` }}
                          />
                        </div>
                        <span className="session-progress">{session.progress.toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReadingProgress;
