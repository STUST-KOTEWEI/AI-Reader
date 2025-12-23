import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import MediaControls from '../components/MediaControls';

describe('MediaControls', () => {
  it('應該渲染所有控制按鈕', () => {
    render(<MediaControls />);
    
    expect(screen.getByRole('button', { name: /掃描/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /播放/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '停止' })).toBeInTheDocument();
  });

  it('點擊掃描按鈕應該呼叫 onScan', () => {
    const onScan = vi.fn();
    render(<MediaControls onScan={onScan} />);
    
    const scanButton = screen.getByRole('button', { name: /掃描/ });
    fireEvent.click(scanButton);
    
    expect(onScan).toHaveBeenCalledTimes(1);
  });

  it('點擊播放按鈕應該呼叫 onPlay', () => {
    const onPlay = vi.fn();
    render(<MediaControls onPlay={onPlay} />);
    
    const playButton = screen.getByRole('button', { name: /播放/ });
    fireEvent.click(playButton);
    
    expect(onPlay).toHaveBeenCalledTimes(1);
  });

  it('點擊停止按鈕應該呼叫 onStop', () => {
    const onStop = vi.fn();
    render(<MediaControls onStop={onStop} isPlaying={true} />);
    
    const stopButton = screen.getByRole('button', { name: '停止' });
    fireEvent.click(stopButton);
    
    expect(onStop).toHaveBeenCalledTimes(1);
  });

  it('播放中時應該顯示暫停按鈕', () => {
    render(<MediaControls isPlaying={true} />);
    
    expect(screen.getByRole('button', { name: '暫停' })).toBeInTheDocument();
  });

  it('暫停時應該顯示播放按鈕', () => {
    render(<MediaControls isPlaying={false} />);
    
    const playButton = screen.getByRole('button', { name: /播放/ });
    expect(playButton).toBeInTheDocument();
  });

  it('掃描中時應該顯示掃描中狀態', () => {
    render(<MediaControls isScanning={true} />);
    
    expect(screen.getByRole('button', { name: '掃描中' })).toBeInTheDocument();
  });

  it('disabled 時所有按鈕應該被停用', () => {
    render(<MediaControls disabled={true} />);
    
    const scanButton = screen.getByRole('button', { name: /掃描/ });
    const playButton = screen.getByRole('button', { name: /播放/ });
    const stopButton = screen.getByRole('button', { name: '停止' });
    
    expect(scanButton).toBeDisabled();
    expect(playButton).toBeDisabled();
    expect(stopButton).toBeDisabled();
  });

  it('應該包含播放速度控制', () => {
    render(<MediaControls />);
    
    expect(screen.getByLabelText('播放速度')).toBeInTheDocument();
    expect(screen.getByRole('slider')).toBeInTheDocument();
  });

  it('應該包含鍵盤快捷鍵說明', () => {
    render(<MediaControls />);
    
    expect(screen.getByText('鍵盤快捷鍵')).toBeInTheDocument();
  });

  it('調整速度滑桿應該更新速度值', () => {
    render(<MediaControls />);
    
    const slider = screen.getByRole('slider');
    fireEvent.change(slider, { target: { value: '1.5' } });
    
    expect(screen.getByText('1.5x')).toBeInTheDocument();
  });

  it('應該有正確的 ARIA 屬性', () => {
    render(<MediaControls isPlaying={true} />);
    
    const controlsGroup = screen.getByRole('group', { name: '媒體控制' });
    expect(controlsGroup).toBeInTheDocument();
    
    const playButton = screen.getByRole('button', { name: '暫停' });
    expect(playButton).toHaveAttribute('aria-pressed', 'true');
  });
});
