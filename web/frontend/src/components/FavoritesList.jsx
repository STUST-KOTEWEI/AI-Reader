import { useState, useEffect } from 'react';
import './FavoritesList.css';
import { t } from '../i18n/translations';

const API_URL = 'http://127.0.0.1:8000';

/**
 * FavoritesList Component
 * 
 * Displays user's bookmarks and favorites.
 */
function FavoritesList({ isOpen, onClose, language = 'zh-tw', userId = 'default' }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('favorites');

  useEffect(() => {
    if (isOpen) {
      fetchBookmarks();
    }
  }, [isOpen]);

  const fetchBookmarks = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_URL}/bookmarks/${userId}`);
      if (!response.ok) {
        throw new Error('無法載入收藏清單');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFavorite = async (favoriteId) => {
    try {
      const response = await fetch(`${API_URL}/bookmarks/${userId}/favorite/${favoriteId}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        fetchBookmarks();
      }
    } catch (err) {
      setError('刪除失敗');
    }
  };

  const handleRemoveBookmark = async (bookmarkId) => {
    try {
      const response = await fetch(`${API_URL}/bookmarks/${userId}/bookmark/${bookmarkId}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        fetchBookmarks();
      }
    } catch (err) {
      setError('刪除失敗');
    }
  };

  const renderStars = (rating) => {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  };

  if (!isOpen) return null;

  const translations = {
    'zh-tw': {
      title: '我的收藏',
      favorites: '收藏清單',
      bookmarks: '書籤',
      noFavorites: '尚無收藏內容',
      noBookmarks: '尚無書籤',
      remove: '移除',
      position: '位置',
      note: '筆記'
    },
    'en': {
      title: 'My Collection',
      favorites: 'Favorites',
      bookmarks: 'Bookmarks',
      noFavorites: 'No favorites yet',
      noBookmarks: 'No bookmarks yet',
      remove: 'Remove',
      position: 'Position',
      note: 'Note'
    },
    'ja': {
      title: 'マイコレクション',
      favorites: 'お気に入り',
      bookmarks: 'ブックマーク',
      noFavorites: 'お気に入りがありません',
      noBookmarks: 'ブックマークがありません',
      remove: '削除',
      position: '位置',
      note: 'メモ'
    },
    'zh-cn': {
      title: '我的收藏',
      favorites: '收藏列表',
      bookmarks: '书签',
      noFavorites: '暂无收藏内容',
      noBookmarks: '暂无书签',
      remove: '移除',
      position: '位置',
      note: '笔记'
    }
  };

  const tr = translations[language] || translations['zh-tw'];

  return (
    <div className="favorites-overlay" onClick={onClose}>
      <div className="favorites-panel" onClick={(e) => e.stopPropagation()}>
        <div className="favorites-header">
          <h2>{tr.title}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'favorites' ? 'active' : ''}`}
            onClick={() => setActiveTab('favorites')}
          >
            ❤️ {tr.favorites}
          </button>
          <button 
            className={`tab ${activeTab === 'bookmarks' ? 'active' : ''}`}
            onClick={() => setActiveTab('bookmarks')}
          >
            🔖 {tr.bookmarks}
          </button>
        </div>

        {loading && <p className="loading">載入中...</p>}
        {error && <p className="error-message">{error}</p>}

        {data && (
          <div className="favorites-content">
            {activeTab === 'favorites' && (
              <div className="favorites-list">
                {data.favorites.length === 0 ? (
                  <p className="no-data">{tr.noFavorites}</p>
                ) : (
                  data.favorites.map((item, index) => (
                    <div key={index} className="favorite-item">
                      <div className="item-icon">📚</div>
                      <div className="item-info">
                        <span className="item-title">{item.content_title}</span>
                        <span className="item-type">{item.content_type}</span>
                        {item.rating > 0 && (
                          <span className="item-rating">{renderStars(item.rating)}</span>
                        )}
                      </div>
                      <button 
                        className="remove-btn"
                        onClick={() => handleRemoveFavorite(item.favorite_id)}
                        title={tr.remove}
                      >
                        🗑️
                      </button>
                    </div>
                  ))
                )}
              </div>
            )}

            {activeTab === 'bookmarks' && (
              <div className="bookmarks-list">
                {data.bookmarks.length === 0 ? (
                  <p className="no-data">{tr.noBookmarks}</p>
                ) : (
                  data.bookmarks.map((item, index) => (
                    <div key={index} className="bookmark-item">
                      <div className="item-icon">🔖</div>
                      <div className="item-info">
                        <span className="item-title">{item.content_title}</span>
                        {item.position && (
                          <span className="item-position">{tr.position}: {item.position}</span>
                        )}
                        {item.note && (
                          <span className="item-note">{tr.note}: {item.note}</span>
                        )}
                        {item.tags && item.tags.length > 0 && (
                          <div className="item-tags">
                            {item.tags.map((tag, i) => (
                              <span key={i} className="tag">{tag}</span>
                            ))}
                          </div>
                        )}
                      </div>
                      <button 
                        className="remove-btn"
                        onClick={() => handleRemoveBookmark(item.bookmark_id)}
                        title={tr.remove}
                      >
                        🗑️
                      </button>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default FavoritesList;
