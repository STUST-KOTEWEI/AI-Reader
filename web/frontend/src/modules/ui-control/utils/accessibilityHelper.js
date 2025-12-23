/**
 * 無障礙輔助工具
 * 提供應用無障礙設定的工具函數
 */

/**
 * 應用無障礙設定到頁面
 * @param {Object} settings - 無障礙設定物件
 */
export function applyAccessibilitySettings(settings) {
  const body = document.body;

  // 移除所有相關的 class
  body.classList.remove(
    'font-small',
    'font-medium',
    'font-large',
    'font-xlarge',
    'high-contrast',
    'inverted',
    'reduced-motion'
  );

  // 應用字型大小
  if (settings.fontSize) {
    body.classList.add(`font-${settings.fontSize}`);
  }

  // 應用對比度設定
  if (settings.contrast === 'high') {
    body.classList.add('high-contrast');
  } else if (settings.contrast === 'inverted') {
    body.classList.add('inverted');
  }

  // 應用減少動畫設定
  if (settings.reducedMotion) {
    body.classList.add('reduced-motion');
  }

  // 更新 CSS 變數
  if (settings.reducedMotion) {
    document.documentElement.style.setProperty('--animation-duration', '0.01ms');
  } else {
    document.documentElement.style.removeProperty('--animation-duration');
  }
}

/**
 * 宣告頁面區域的 ARIA 標籤
 * @param {string} selector - CSS 選擇器
 * @param {string} role - ARIA 角色
 * @param {string} label - ARIA 標籤
 */
export function announceToScreenReader(message, priority = 'polite') {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  // 在短暫延遲後移除元素
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
}

/**
 * 管理焦點指示器
 * @param {boolean} enhanced - 是否使用增強型焦點指示器
 */
export function setFocusIndicator(enhanced) {
  if (enhanced) {
    document.documentElement.style.setProperty('--focus-outline-width', '3px');
    document.documentElement.style.setProperty('--focus-outline-offset', '3px');
  } else {
    document.documentElement.style.setProperty('--focus-outline-width', '2px');
    document.documentElement.style.setProperty('--focus-outline-offset', '2px');
  }
}

/**
 * 檢測使用者的偏好設定
 * @returns {Object} 系統偏好設定
 */
export function detectSystemPreferences() {
  return {
    reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    highContrast: window.matchMedia('(prefers-contrast: high)').matches,
    darkMode: window.matchMedia('(prefers-color-scheme: dark)').matches,
  };
}

/**
 * 跳轉到主要內容
 */
export function skipToMainContent() {
  const main = document.querySelector('main') || document.querySelector('[role="main"]');
  if (main) {
    main.setAttribute('tabindex', '-1');
    main.focus();
  }
}
