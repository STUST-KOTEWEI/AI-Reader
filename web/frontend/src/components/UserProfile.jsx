import { useState, useEffect, useCallback } from 'react';
import './UserProfile.css';
import { t } from '../i18n/translations';

const API_URL = 'http://127.0.0.1:8000';

/**
 * UserProfile Component
 * 
 * Provides user profile settings panel with accessibility options.
 */
function UserProfile({ onProfileChange, isOpen, onClose, language = 'zh-tw' }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [currentLang, setCurrentLang] = useState(language);

  // Update currentLang when language prop changes
  useEffect(() => {
    setCurrentLang(language);
  }, [language]);

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
        throw new Error(t(currentLang, 'loadError'));
      }
      const data = await response.json();
      setProfile(data);
      // Update current language from profile
      if (data.preferences?.preferred_language) {
        setCurrentLang(data.preferences.preferred_language);
      }
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
        throw new Error(t(currentLang, 'saveError'));
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
    // Update current language immediately when language preference changes
    if (key === 'preferred_language') {
      setCurrentLang(value);
    }
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
          <h2 id="profile-title">{t(currentLang, 'userSettings')}</h2>
          <button 
            className="close-button" 
            onClick={onClose}
            aria-label={t(currentLang, 'closePanel')}
          >
            ✕
          </button>
        </div>

        {loading && <p className="loading" aria-live="polite">{t(currentLang, 'loading')}</p>}
        {error && <p className="error-message" role="alert">{error}</p>}

        {profile && (
          <div className="profile-content">
            {/* Display Name */}
            <div className="profile-section">
              <h3>{t(currentLang, 'basicSettings')}</h3>
              <label htmlFor="display-name">
                {t(currentLang, 'displayName')}
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
              <h3>{t(currentLang, 'accessibilitySettings')}</h3>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.haptic_enabled}
                  onChange={(e) =>
                    updateAccessibility('haptic_enabled', e.target.checked)
                  }
                />
                {t(currentLang, 'enableHaptic')}
              </label>

              {profile.accessibility.haptic_enabled && (
                <label>
                  {t(currentLang, 'hapticIntensity')}
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
                {t(currentLang, 'enableAudio')}
              </label>

              {profile.accessibility.audio_enabled && (
                <label>
                  {t(currentLang, 'audioSpeed')}
                  <select
                    value={profile.accessibility.audio_speed}
                    onChange={(e) =>
                      updateAccessibility(
                        'audio_speed',
                        parseFloat(e.target.value)
                      )
                    }
                  >
                    <option value="0.75">{t(currentLang, 'slowSpeed')} (0.75x)</option>
                    <option value="1.0">{t(currentLang, 'normalSpeed')} (1x)</option>
                    <option value="1.25">{t(currentLang, 'fastSpeed')} (1.25x)</option>
                    <option value="1.5">{t(currentLang, 'veryFastSpeed')} (1.5x)</option>
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
                {t(currentLang, 'highContrast')}
              </label>

              <label>
                {t(currentLang, 'fontSize')}
                <select
                  value={profile.accessibility.font_size}
                  onChange={(e) =>
                    updateAccessibility('font_size', parseInt(e.target.value))
                  }
                >
                  <option value="12">{t(currentLang, 'fontSmall')} (12px)</option>
                  <option value="16">{t(currentLang, 'fontMedium')} (16px)</option>
                  <option value="20">{t(currentLang, 'fontLarge')} (20px)</option>
                  <option value="24">{t(currentLang, 'fontExtraLarge')} (24px)</option>
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
                {t(currentLang, 'reduceMotion')}
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.accessibility.screen_reader_mode}
                  onChange={(e) =>
                    updateAccessibility('screen_reader_mode', e.target.checked)
                  }
                />
                {t(currentLang, 'screenReaderMode')}
              </label>
            </div>

            {/* User Preferences */}
            <div className="profile-section">
              <h3>{t(currentLang, 'preferences')}</h3>

              <label>
                {t(currentLang, 'preferredLanguage')}
                <select
                  value={profile.preferences.preferred_language}
                  onChange={(e) =>
                    updatePreferences('preferred_language', e.target.value)
                  }
                >
                  <option value="zh-tw">繁體中文</option>
                  <option value="zh-cn">简体中文</option>
                  <option value="en">English</option>
                  <option value="ja">日本語</option>
                </select>
              </label>

              <label>
                {t(currentLang, 'theme')}
                <select
                  value={profile.preferences.theme}
                  onChange={(e) =>
                    updatePreferences('theme', e.target.value)
                  }
                >
                  <option value="dark">{t(currentLang, 'themeDark')}</option>
                  <option value="light">{t(currentLang, 'themeLight')}</option>
                  <option value="auto">{t(currentLang, 'themeAuto')}</option>
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
                {t(currentLang, 'autoPlayAudio')}
              </label>

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={profile.preferences.save_history}
                  onChange={(e) =>
                    updatePreferences('save_history', e.target.checked)
                  }
                />
                {t(currentLang, 'saveHistory')}
              </label>
            </div>

            {/* Save Button */}
            <div className="profile-actions">
              <button
                className="save-button"
                onClick={saveProfile}
                disabled={saving}
              >
                {saving ? t(currentLang, 'saving') : t(currentLang, 'save')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default UserProfile;
