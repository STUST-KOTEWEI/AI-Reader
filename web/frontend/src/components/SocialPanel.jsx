import { useState, useEffect } from 'react';
import './SocialPanel.css';

const API_URL = 'http://127.0.0.1:8000';

const translations = {
  'zh-tw': {
    title: '社群互動',
    comments: '評論',
    share: '分享',
    statistics: '統計',
    writeComment: '寫下您的評論...',
    postComment: '發布評論',
    posting: '發布中...',
    noComments: '暫無評論，成為第一個評論者！',
    views: '瀏覽次數',
    shares: '分享次數',
    likes: '喜歡',
    shareToTwitter: '分享到 Twitter',
    shareToFacebook: '分享到 Facebook',
    shareToLine: '分享到 LINE',
    copyLink: '複製連結',
    linkCopied: '連結已複製！',
    loginToComment: '登入後即可評論',
    reply: '回覆',
    like: '讚'
  },
  'zh-cn': {
    title: '社区互动',
    comments: '评论',
    share: '分享',
    statistics: '统计',
    writeComment: '写下您的评论...',
    postComment: '发布评论',
    posting: '发布中...',
    noComments: '暂无评论，成为第一个评论者！',
    views: '浏览次数',
    shares: '分享次数',
    likes: '喜欢',
    shareToTwitter: '分享到 Twitter',
    shareToFacebook: '分享到 Facebook',
    shareToLine: '分享到 LINE',
    copyLink: '复制链接',
    linkCopied: '链接已复制！',
    loginToComment: '登录后即可评论',
    reply: '回复',
    like: '赞'
  },
  'en': {
    title: 'Social',
    comments: 'Comments',
    share: 'Share',
    statistics: 'Statistics',
    writeComment: 'Write a comment...',
    postComment: 'Post Comment',
    posting: 'Posting...',
    noComments: 'No comments yet. Be the first to comment!',
    views: 'Views',
    shares: 'Shares',
    likes: 'Likes',
    shareToTwitter: 'Share to Twitter',
    shareToFacebook: 'Share to Facebook',
    shareToLine: 'Share to LINE',
    copyLink: 'Copy Link',
    linkCopied: 'Link copied!',
    loginToComment: 'Login to comment',
    reply: 'Reply',
    like: 'Like'
  },
  'ja': {
    title: 'コミュニティ',
    comments: 'コメント',
    share: '共有',
    statistics: '統計',
    writeComment: 'コメントを書く...',
    postComment: 'コメントを投稿',
    posting: '投稿中...',
    noComments: 'コメントはまだありません。最初のコメントを書こう！',
    views: '閲覧数',
    shares: '共有数',
    likes: 'いいね',
    shareToTwitter: 'Twitterで共有',
    shareToFacebook: 'Facebookで共有',
    shareToLine: 'LINEで共有',
    copyLink: 'リンクをコピー',
    linkCopied: 'リンクをコピーしました！',
    loginToComment: 'ログインしてコメント',
    reply: '返信',
    like: 'いいね'
  }
};

function SocialPanel({ isOpen, onClose, language = 'zh-tw', userId, contentId }) {
  const tr = translations[language] || translations['zh-tw'];
  const [activeTab, setActiveTab] = useState('comments');
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [posting, setPosting] = useState(false);
  const [stats, setStats] = useState({ views: 0, shares: 0, likes: 0 });
  const [linkCopied, setLinkCopied] = useState(false);

  useEffect(() => {
    if (isOpen && contentId) {
      fetchComments();
      fetchStats();
    }
  }, [isOpen, contentId]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const fetchComments = async () => {
    if (!contentId) return;
    try {
      const response = await fetch(`${API_URL}/social/comments/${contentId}`);
      if (response.ok) {
        const data = await response.json();
        setComments(data.comments || []);
      }
    } catch (err) {
      console.error('Failed to fetch comments:', err);
    }
  };

  const fetchStats = async () => {
    if (!contentId) return;
    try {
      const response = await fetch(`${API_URL}/social/stats/${contentId}`);
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  const postComment = async () => {
    if (!userId || !contentId || !newComment.trim()) return;
    setPosting(true);
    try {
      const response = await fetch(`${API_URL}/social/comments/${contentId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          text: newComment.trim()
        })
      });
      if (response.ok) {
        setNewComment('');
        fetchComments();
      }
    } catch (err) {
      console.error('Failed to post comment:', err);
    } finally {
      setPosting(false);
    }
  };

  const shareToSocial = async (platform) => {
    const url = window.location.href;
    const text = 'Check out this amazing immersive experience!';
    
    let shareUrl;
    switch (platform) {
      case 'twitter':
        shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
        break;
      case 'facebook':
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
        break;
      case 'line':
        shareUrl = `https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(url)}`;
        break;
      default:
        return;
    }

    window.open(shareUrl, '_blank', 'width=600,height=400');
    
    // Record share
    if (userId && contentId) {
      try {
        await fetch(`${API_URL}/social/share`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: userId,
            content_id: contentId,
            platform
          })
        });
        fetchStats();
      } catch (err) {
        console.error('Failed to record share:', err);
      }
    }
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy link:', err);
    }
  };

  const likeComment = async (commentId) => {
    if (!userId) return;
    try {
      await fetch(`${API_URL}/social/comments/${contentId}/${commentId}/like`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      });
      fetchComments();
    } catch (err) {
      console.error('Failed to like comment:', err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="social-overlay" onClick={onClose}>
      <div 
        className="social-panel" 
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-label={tr.title}
      >
        <header className="social-header">
          <h2>{tr.title}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </header>

        <div className="social-tabs">
          <button 
            className={`tab-button ${activeTab === 'comments' ? 'active' : ''}`}
            onClick={() => setActiveTab('comments')}
          >
            💬 {tr.comments}
          </button>
          <button 
            className={`tab-button ${activeTab === 'share' ? 'active' : ''}`}
            onClick={() => setActiveTab('share')}
          >
            📤 {tr.share}
          </button>
          <button 
            className={`tab-button ${activeTab === 'stats' ? 'active' : ''}`}
            onClick={() => setActiveTab('stats')}
          >
            📊 {tr.statistics}
          </button>
        </div>

        <div className="social-content">
          {/* Comments Tab */}
          {activeTab === 'comments' && (
            <div className="comments-section">
              {userId ? (
                <div className="comment-input">
                  <textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder={tr.writeComment}
                    rows="3"
                    disabled={posting}
                  />
                  <button 
                    className="post-button"
                    onClick={postComment}
                    disabled={posting || !newComment.trim()}
                  >
                    {posting ? tr.posting : tr.postComment}
                  </button>
                </div>
              ) : (
                <div className="login-prompt">
                  <p>{tr.loginToComment}</p>
                </div>
              )}

              <div className="comments-list">
                {comments.length === 0 ? (
                  <div className="empty-comments">
                    <span className="empty-icon">💬</span>
                    <p>{tr.noComments}</p>
                  </div>
                ) : (
                  comments.map(comment => (
                    <div key={comment.id} className="comment-item">
                      <div className="comment-avatar">
                        {comment.username?.[0]?.toUpperCase() || '?'}
                      </div>
                      <div className="comment-body">
                        <div className="comment-header">
                          <span className="comment-author">{comment.username || 'Anonymous'}</span>
                          <span className="comment-time">{new Date(comment.created_at).toLocaleDateString()}</span>
                        </div>
                        <p className="comment-text">{comment.text}</p>
                        <div className="comment-actions">
                          <button 
                            className="action-btn"
                            onClick={() => likeComment(comment.id)}
                          >
                            👍 {tr.like} {comment.likes > 0 && `(${comment.likes})`}
                          </button>
                          <button className="action-btn">
                            💬 {tr.reply}
                          </button>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Share Tab */}
          {activeTab === 'share' && (
            <div className="share-section">
              <div className="share-buttons">
                <button 
                  className="share-btn twitter"
                  onClick={() => shareToSocial('twitter')}
                >
                  <span className="share-icon">🐦</span>
                  {tr.shareToTwitter}
                </button>
                <button 
                  className="share-btn facebook"
                  onClick={() => shareToSocial('facebook')}
                >
                  <span className="share-icon">📘</span>
                  {tr.shareToFacebook}
                </button>
                <button 
                  className="share-btn line"
                  onClick={() => shareToSocial('line')}
                >
                  <span className="share-icon">💚</span>
                  {tr.shareToLine}
                </button>
                <button 
                  className="share-btn copy"
                  onClick={copyLink}
                >
                  <span className="share-icon">🔗</span>
                  {linkCopied ? tr.linkCopied : tr.copyLink}
                </button>
              </div>
            </div>
          )}

          {/* Statistics Tab */}
          {activeTab === 'stats' && (
            <div className="stats-section">
              <div className="stat-card">
                <span className="stat-icon">👁️</span>
                <div className="stat-info">
                  <span className="stat-value">{stats.views || 0}</span>
                  <span className="stat-label">{tr.views}</span>
                </div>
              </div>
              <div className="stat-card">
                <span className="stat-icon">📤</span>
                <div className="stat-info">
                  <span className="stat-value">{stats.shares || 0}</span>
                  <span className="stat-label">{tr.shares}</span>
                </div>
              </div>
              <div className="stat-card">
                <span className="stat-icon">❤️</span>
                <div className="stat-info">
                  <span className="stat-value">{stats.likes || 0}</span>
                  <span className="stat-label">{tr.likes}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SocialPanel;
