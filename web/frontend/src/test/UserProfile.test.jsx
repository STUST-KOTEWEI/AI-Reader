import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import UserProfile from '../components/UserProfile';

// Mock fetch API
const mockProfile = {
  user_id: 'default',
  display_name: '使用者',
  accessibility: {
    haptic_enabled: true,
    haptic_intensity: 0.6,
    audio_enabled: true,
    audio_speed: 1.0,
    high_contrast: false,
    font_size: 16,
    reduce_motion: false,
    screen_reader_mode: false,
  },
  preferences: {
    preferred_language: 'zh-tw',
    preferred_voice: null,
    theme: 'dark',
    auto_play_audio: false,
    save_history: true,
  },
};

describe('UserProfile', () => {
  beforeEach(() => {
    // Mock fetch for profile API
    globalThis.fetch = vi.fn((url) => {
      if (url.includes('/profile')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockProfile),
        });
      }
      return Promise.reject(new Error('Unknown URL'));
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('不應該在關閉狀態時渲染', () => {
    render(
      <UserProfile isOpen={false} onClose={() => {}} onProfileChange={() => {}} />
    );
    expect(screen.queryByText('使用者設定')).not.toBeInTheDocument();
  });

  it('應該在開啟狀態時渲染標題', async () => {
    render(
      <UserProfile isOpen={true} onClose={() => {}} onProfileChange={() => {}} />
    );
    await waitFor(() => {
      expect(screen.getByText('使用者設定')).toBeInTheDocument();
    });
  });

  it('應該載入並顯示使用者設定', async () => {
    render(
      <UserProfile isOpen={true} onClose={() => {}} onProfileChange={() => {}} />
    );
    
    await waitFor(() => {
      expect(screen.getByText('基本設定')).toBeInTheDocument();
      expect(screen.getByText('無障礙設定')).toBeInTheDocument();
      expect(screen.getByText('偏好設定')).toBeInTheDocument();
    });
  });

  it('應該顯示無障礙設定選項', async () => {
    render(
      <UserProfile isOpen={true} onClose={() => {}} onProfileChange={() => {}} />
    );
    
    await waitFor(() => {
      expect(screen.getByText('啟用觸覺回饋')).toBeInTheDocument();
      expect(screen.getByText('啟用語音輸出')).toBeInTheDocument();
      expect(screen.getByText('高對比模式')).toBeInTheDocument();
      expect(screen.getByText('減少動態效果')).toBeInTheDocument();
    });
  });

  it('應該在點擊關閉按鈕時呼叫 onClose', async () => {
    const onClose = vi.fn();
    render(
      <UserProfile isOpen={true} onClose={onClose} onProfileChange={() => {}} />
    );
    
    await waitFor(() => {
      expect(screen.getByText('使用者設定')).toBeInTheDocument();
    });
    
    const closeButton = screen.getByText('✕');
    fireEvent.click(closeButton);
    expect(onClose).toHaveBeenCalled();
  });

  it('應該顯示儲存按鈕', async () => {
    render(
      <UserProfile isOpen={true} onClose={() => {}} onProfileChange={() => {}} />
    );
    
    await waitFor(() => {
      expect(screen.getByText('儲存設定')).toBeInTheDocument();
    });
  });
});
