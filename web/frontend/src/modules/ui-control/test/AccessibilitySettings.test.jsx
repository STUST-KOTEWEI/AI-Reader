import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import AccessibilitySettings from '../components/AccessibilitySettings';

describe('AccessibilitySettings', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('應該渲染無障礙設定按鈕', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    expect(button).toBeInTheDocument();
  });

  it('點擊按鈕後應該顯示設定面板', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    
    fireEvent.click(button);
    
    const panel = screen.getByRole('dialog');
    expect(panel).toBeInTheDocument();
    expect(panel).toHaveAttribute('aria-labelledby', 'accessibility-title');
  });

  it('應該包含字型大小選項', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    expect(screen.getByText('字型大小')).toBeInTheDocument();
    expect(screen.getByText('小')).toBeInTheDocument();
    expect(screen.getByText('中')).toBeInTheDocument();
    expect(screen.getByText('大')).toBeInTheDocument();
    expect(screen.getByText('特大')).toBeInTheDocument();
  });

  it('應該包含對比度選項', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    expect(screen.getByText('對比度')).toBeInTheDocument();
    expect(screen.getByText('正常')).toBeInTheDocument();
    expect(screen.getByText('高對比')).toBeInTheDocument();
    expect(screen.getByText('反相')).toBeInTheDocument();
  });

  it('應該包含減少動畫選項', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    expect(screen.getByText('減少動畫效果')).toBeInTheDocument();
  });

  it('應該包含螢幕閱讀器優化選項', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    expect(screen.getByText('螢幕閱讀器優化')).toBeInTheDocument();
  });

  it('應該包含鍵盤導航增強選項', () => {
    render(<AccessibilitySettings />);
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    expect(screen.getByText('鍵盤導航增強')).toBeInTheDocument();
  });

  it('設定變更時應該呼叫回調函數', () => {
    const onSettingsChange = vi.fn();
    render(<AccessibilitySettings onSettingsChange={onSettingsChange} />);
    
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    const largeRadio = screen.getByLabelText('大');
    fireEvent.click(largeRadio);
    
    expect(onSettingsChange).toHaveBeenCalled();
  });

  it('應該將設定儲存到 localStorage', () => {
    render(<AccessibilitySettings />);
    
    const button = screen.getByLabelText('無障礙設定');
    fireEvent.click(button);
    
    const largeRadio = screen.getByLabelText('大');
    fireEvent.click(largeRadio);
    
    const saved = localStorage.getItem('accessibility-settings');
    expect(saved).toBeTruthy();
    const settings = JSON.parse(saved);
    expect(settings.fontSize).toBe('large');
  });

  it('關閉按鈕應該隱藏面板', () => {
    render(<AccessibilitySettings />);
    
    const openButton = screen.getByLabelText('無障礙設定');
    fireEvent.click(openButton);
    
    const closeButton = screen.getByLabelText('關閉設定');
    fireEvent.click(closeButton);
    
    const panel = screen.queryByRole('dialog');
    expect(panel).not.toBeInTheDocument();
  });
});
