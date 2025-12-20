import { useState, useEffect, useCallback } from 'react';
import './UserProfile.css';

const API_URL = 'http://127.0.0.1:8000';

/**
 * UserProfile Component
 * 
 * Provides user profile settings panel with accessibility options.
 */
function UserProfile({ onProfileChange, isOpen, onClose }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  // Handle Escape key to close the modal
  const handleKeyDown = useCallback((event) => {
    if (event.key === 'Escape') {
      onClose();
    }
  }, [onClose]);

  // Add keyboard event listener when open
  useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      return () => {
        document.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [isOpen, handleKeyDown]);

  // Fetch profile on mount
  useEffect(() => {
    if (isOpen) {
      fetchProfile();
    }
  }, [isOpen]);

  const fetchProfile = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_URL}/profile`);
      if (!response.ok) {
        throw new Error('無法載入使用者設定');
      }
      const data = await response.json();
      setProfile(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const saveProfile = async () => {
    setSaving(true);
    setError('');
    try {
      const response = await fetch(`${API_URL}/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          display_name: profile.display_name,
          accessibility: profile.accessibility,
          preferences: profile.preferences,
        }),
      });
      if (!response.ok) {
        throw new Error('無法儲存設定');
      }
      const data = await response.json();
      setProfile(data);
      if (onProfileChange) {
        onProfileChange(data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const updateAccessibility = (key, value) => {
    setProfile((prev) => ({
      ...prev,
      accessibility: {
        ...prev.accessibility,
        [key]: value,
      },
    }));
  };

  const updatePreferences = (key, value) => {
    setProfile((prev) => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [key]: value,
      },
    }));
  };

  if (!isOpen) return null;

  return (
    <div 
      className="profile-overlay" 
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="profile-title"
    >
      <div className="profile-panel" onClick={(e) => e.stopPropagation()}>
        <div className="profile-header">
          <h2 id="profile-title">使用者設定</h2>
          <button 
            className="close-button" 
            onClick={onClose}
            aria-label="關閉設定面板"
          >
            ✕
          </button>
        </div>

        {loading && <p className="loading" aria-live="polite">載入中...</p>}
        {error && <p className="error-message" role="alert">{error}</p>}

        {profile && (
          <div className="profile-content">
            {/* Display Name */}
            <div className="profile-section">
              <h3>基本設定</h3>
              <label htmlFor="display-name">
                顯示名稱
                <input
                  id="display-name"
                  type="text"
                  value={profile.display_name}
                  onChange={(e) =>
                    setProfile((prev) => ({
                      ...prev,
                      display_name: e.target.value,
                    }))
                  }
                />
              </label>
            </div>

            {/* Accessibility Settings */}
            <div className="profile-section">
              <h3>無障礙設定</h3>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.haptic_enabled}
                  onChange={(e) =>
                    updateAccessibility('haptic_enabled', e.target.checked)
                  }
                />
                啟用觸覺回饋
              </label>

              {profile.accessibility.haptic_enabled && (
                <label>
                  觸覺強度
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={profile.accessibility.haptic_intensity}
                    onChange={(e) =>
                      updateAccessibility(
                        'haptic_intensity',
                        parseFloat(e.target.value)
                      )
                    }
                  />
                  <span>{Math.round(profile.accessibility.haptic_intensity * 100)}%</span>
                </label>
              )}

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.audio_enabled}
                  onChange={(e) =>
                    updateAccessibility('audio_enabled', e.target.checked)
                  }
                />
                啟用語音輸出
              </label>

              {profile.accessibility.audio_enabled && (
                <label>
                  語音速度
                  <select
                    value={profile.accessibility.audio_speed}
                    onChange={(e) =>
                      updateAccessibility(
                        'audio_speed',
                        parseFloat(e.target.value)
                      )
                    }
                  >
                    <option value="0.75">慢速 (0.75x)</option>
                    <option value="1.0">正常 (1x)</option>
                    <option value="1.25">快速 (1.25x)</option>
                    <option value="1.5">極快 (1.5x)</option>
                  </select>
                </label>
              )}

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.high_contrast}
                  onChange={(e) =>
                    updateAccessibility('high_contrast', e.target.checked)
                  }
                />
                高對比模式
              </label>

              <label>
                字體大小
                <select
                  value={profile.accessibility.font_size}
                  onChange={(e) =>
                    updateAccessibility('font_size', parseInt(e.target.value))
                  }
                >
                  <option value="12">小 (12px)</option>
                  <option value="16">中 (16px)</option>
                  <option value="20">大 (20px)</option>
                  <option value="24">特大 (24px)</option>
                </select>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.reduce_motion}
                  onChange={(e) =>
                    updateAccessibility('reduce_motion', e.target.checked)
                  }
                />
                減少動態效果
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.screen_reader_mode}
                  onChange={(e) =>
                    updateAccessibility('screen_reader_mode', e.target.checked)
                  }
                />
                螢幕閱讀器模式
              </label>
            </div>

            {/* User Preferences */}
            <div className="profile-section">
              <h3>偏好設定</h3>

              <label>
                偏好語言
                <select
                  value={profile.preferences.preferred_language}
                  onChange={(e) =>
                    updatePreferences('preferred_language', e.target.value)
                  }
                >
                  <option value="zh-tw">繁體中文</option>
                  <option value="zh-cn">簡體中文</option>
                  <option value="en">English</option>
                  <option value="ja">日本語</option>
                </select>
              </label>

              <label>
                主題
                <select
                  value={profile.preferences.theme}
                  onChange={(e) =>
                    updatePreferences('theme', e.target.value)
                  }
                >
                  <option value="dark">深色</option>
                  <option value="light">淺色</option>
                  <option value="auto">自動</option>
                </select>
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.preferences.auto_play_audio}
                  onChange={(e) =>
                    updatePreferences('auto_play_audio', e.target.checked)
                  }
                />
                自動播放語音
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.preferences.save_history}
                  onChange={(e) =>
                    updatePreferences('save_history', e.target.checked)
                  }
                />
                儲存閱讀歷史
              </label>
            </div>

            {/* Save Button */}
            <div className="profile-actions">
              <button
                className="save-button"
                onClick={saveProfile}
                disabled={saving}
              >
                {saving ? '儲存中...' : '儲存設定'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default UserProfile;
