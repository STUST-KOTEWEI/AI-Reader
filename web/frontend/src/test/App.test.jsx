import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('應該要能渲染標題', () => {
    render(<App />);
    
    // 使用 screen.getByRole 來尋找 heading 元素
    const headingElement = screen.getByRole('heading', { name: /AI多感官智能閱讀器/i, level: 1 });
    
    // 斷言元素存在於文件中
    expect(headingElement).toBeInTheDocument();
  });

  it('應該要顯示文字輸入區', () => {
    render(<App />);
    const textareaElement = screen.getByPlaceholderText(/在這裡輸入您的故事或情境/);
    expect(textareaElement).toBeInTheDocument();
  });
});
