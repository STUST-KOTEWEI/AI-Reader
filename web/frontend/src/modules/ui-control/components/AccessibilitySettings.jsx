import { useState, useEffect } from 'react';
import './AccessibilitySettings.css';

/**
 * 無障礙設定元件
 * 符合 WAI-ARIA 1.2 標準，提供個人化無障礙設定
 */
function AccessibilitySettings({ onSettingsChange }) {
  const [settings, setSettings] = useState({
    fontSize: 'medium',
    contrast: 'normal',
    reducedMotion: false,
    screenReader: false,
    keyboardNav: true,
  });

  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // 從 localStorage 載入設定
    const savedSettings = localStorage.getItem('accessibility-settings');
    if (savedSettings) {
      const parsed = JSON.parse(savedSettings);
      setSettings(parsed);
      if (onSettingsChange) {
        onSettingsChange(parsed);
      }
    }
  }, [onSettingsChange]);

  const updateSetting = (key, value) => {
    const newSettings = { ...settings, [key]: value };
    setSettings(newSettings);
    localStorage.setItem('accessibility-settings', JSON.stringify(newSettings));
    if (onSettingsChange) {
      onSettingsChange(newSettings);
    }
  };

  return (
    <div className="accessibility-settings">
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls="accessibility-panel"
        className="accessibility-toggle"
        aria-label="無障礙設定"
      >
        <span aria-hidden="true">♿</span>
        <span className="sr-only">開啟無障礙設定</span>
      </button>

      {isOpen && (
        <div
          id="accessibility-panel"
          className="accessibility-panel"
          role="dialog"
          aria-labelledby="accessibility-title"
          aria-modal="true"
        >
          <div className="panel-header">
            <h2 id="accessibility-title">無障礙設定</h2>
            <button
              onClick={() => setIsOpen(false)}
              aria-label="關閉設定"
              className="close-button"
            >
              ✕
            </button>
          </div>

          <div className="settings-group">
            <fieldset>
              <legend>字型大小</legend>
              <div role="radiogroup" aria-labelledby="font-size-label">
                {['small', 'medium', 'large', 'xlarge'].map((size) => (
                  <label key={size} className="radio-label">
                    <input
                      type="radio"
                      name="fontSize"
                      value={size}
                      checked={settings.fontSize === size}
                      onChange={(e) => updateSetting('fontSize', e.target.value)}
                    />
                    <span>{size === 'small' ? '小' : size === 'medium' ? '中' : size === 'large' ? '大' : '特大'}</span>
                  </label>
                ))}
              </div>
            </fieldset>
          </div>

          <div className="settings-group">
            <fieldset>
              <legend>對比度</legend>
              <div role="radiogroup" aria-labelledby="contrast-label">
                {['normal', 'high', 'inverted'].map((contrast) => (
                  <label key={contrast} className="radio-label">
                    <input
                      type="radio"
                      name="contrast"
                      value={contrast}
                      checked={settings.contrast === contrast}
                      onChange={(e) => updateSetting('contrast', e.target.value)}
                    />
                    <span>{contrast === 'normal' ? '正常' : contrast === 'high' ? '高對比' : '反相'}</span>
                  </label>
                ))}
              </div>
            </fieldset>
          </div>

          <div className="settings-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.reducedMotion}
                onChange={(e) => updateSetting('reducedMotion', e.target.checked)}
                aria-describedby="reduced-motion-desc"
              />
              <span>減少動畫效果</span>
            </label>
            <p id="reduced-motion-desc" className="setting-description">
              減少或停用介面動畫，適合對動畫敏感的使用者
            </p>
          </div>

          <div className="settings-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.screenReader}
                onChange={(e) => updateSetting('screenReader', e.target.checked)}
                aria-describedby="screen-reader-desc"
              />
              <span>螢幕閱讀器優化</span>
            </label>
            <p id="screen-reader-desc" className="setting-description">
              啟用額外的螢幕閱讀器支援和語音描述
            </p>
          </div>

          <div className="settings-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.keyboardNav}
                onChange={(e) => updateSetting('keyboardNav', e.target.checked)}
                aria-describedby="keyboard-nav-desc"
              />
              <span>鍵盤導航增強</span>
            </label>
            <p id="keyboard-nav-desc" className="setting-description">
              啟用鍵盤快捷鍵和增強的焦點指示器
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AccessibilitySettings;
