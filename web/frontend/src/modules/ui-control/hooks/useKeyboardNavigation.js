import { useEffect, useCallback } from 'react';

/**
 * 鍵盤導航 Hook
 * 提供鍵盤快捷鍵支援，增強無障礙體驗
 * 
 * @param {Object} callbacks - 鍵盤事件回調函數
 * @param {boolean} enabled - 是否啟用鍵盤導航
 */
function useKeyboardNavigation(callbacks = {}, enabled = true) {
  const {
    onPlay,
    onPause,
    onStop,
    onScan,
    onSpeedUp,
    onSpeedDown,
  } = callbacks;

  const handleKeyDown = useCallback((event) => {
    if (!enabled) return;

    // 避免在輸入元素中觸發快捷鍵
    const target = event.target;
    if (
      target.tagName === 'INPUT' ||
      target.tagName === 'TEXTAREA' ||
      target.isContentEditable
    ) {
      return;
    }

    switch (event.key) {
      case ' ':
      case 'Spacebar':
        event.preventDefault();
        if (onPlay) onPlay();
        if (onPause) onPause();
        break;

      case 'Escape':
        event.preventDefault();
        if (onStop) onStop();
        break;

      case 's':
      case 'S':
        event.preventDefault();
        if (onScan) onScan();
        break;

      case 'ArrowRight':
        event.preventDefault();
        if (onSpeedUp) onSpeedUp();
        break;

      case 'ArrowLeft':
        event.preventDefault();
        if (onSpeedDown) onSpeedDown();
        break;

      default:
        break;
    }
  }, [enabled, onPlay, onPause, onStop, onScan, onSpeedUp, onSpeedDown]);

  useEffect(() => {
    if (enabled) {
      window.addEventListener('keydown', handleKeyDown);
      return () => {
        window.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [enabled, handleKeyDown]);

  return null;
}

export default useKeyboardNavigation;
