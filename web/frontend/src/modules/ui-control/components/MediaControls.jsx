import { useState } from 'react';
import './MediaControls.css';

/**
 * 媒體控制元件
 * 提供掃描、播放與互動控制，符合無障礙設計
 */
function MediaControls({ 
  onScan, 
  onPlay, 
  onPause, 
  onStop,
  isPlaying = false,
  isScanning = false,
  disabled = false
}) {
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);

  const handleScan = () => {
    if (onScan && !disabled) {
      onScan();
    }
  };

  const handlePlayPause = () => {
    if (disabled) return;
    if (isPlaying && onPause) {
      onPause();
    } else if (!isPlaying && onPlay) {
      onPlay();
    }
  };

  const handleStop = () => {
    if (onStop && !disabled) {
      onStop();
    }
  };

  const handleSpeedChange = (e) => {
    const speed = parseFloat(e.target.value);
    setPlaybackSpeed(speed);
  };

  return (
    <div 
      className="media-controls"
      role="group"
      aria-label="媒體控制"
    >
      <div className="controls-main">
        <button
          onClick={handleScan}
          disabled={disabled || isScanning}
          className="control-button scan-button"
          aria-label={isScanning ? '掃描中' : '開始掃描'}
          aria-pressed={isScanning}
        >
          <span aria-hidden="true">📷</span>
          <span className="button-text">
            {isScanning ? '掃描中...' : '掃描'}
          </span>
        </button>

        <button
          onClick={handlePlayPause}
          disabled={disabled}
          className="control-button play-pause-button"
          aria-label={isPlaying ? '暫停' : '播放'}
          aria-pressed={isPlaying}
        >
          <span aria-hidden="true">{isPlaying ? '⏸' : '▶'}</span>
          <span className="button-text">
            {isPlaying ? '暫停' : '播放'}
          </span>
        </button>

        <button
          onClick={handleStop}
          disabled={disabled || (!isPlaying && !isScanning)}
          className="control-button stop-button"
          aria-label="停止"
        >
          <span aria-hidden="true">⏹</span>
          <span className="button-text">停止</span>
        </button>
      </div>

      <div className="controls-secondary">
        <label htmlFor="playback-speed" className="speed-label">
          播放速度
        </label>
        <div className="speed-control">
          <input
            id="playback-speed"
            type="range"
            min="0.5"
            max="2.0"
            step="0.25"
            value={playbackSpeed}
            onChange={handleSpeedChange}
            disabled={disabled}
            aria-valuemin="0.5"
            aria-valuemax="2.0"
            aria-valuenow={playbackSpeed}
            aria-valuetext={`${playbackSpeed}倍速`}
            className="speed-slider"
          />
          <output 
            htmlFor="playback-speed"
            className="speed-value"
            aria-live="polite"
          >
            {playbackSpeed}x
          </output>
        </div>
      </div>

      <div 
        className="keyboard-shortcuts"
        role="complementary"
        aria-label="鍵盤快捷鍵說明"
      >
        <details>
          <summary>鍵盤快捷鍵</summary>
          <ul>
            <li><kbd>Space</kbd> - 播放/暫停</li>
            <li><kbd>S</kbd> - 掃描</li>
            <li><kbd>Esc</kbd> - 停止</li>
            <li><kbd>←/→</kbd> - 調整速度</li>
          </ul>
        </details>
      </div>
    </div>
  );
}

export default MediaControls;
