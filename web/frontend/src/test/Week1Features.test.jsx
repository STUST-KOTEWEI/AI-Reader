import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from '../App';

// Mock fetch globally
global.fetch = vi.fn();

describe('Week 1 Sprint Features', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  it('應該顯示文本分段功能的結果', async () => {
    // Mock API response with segmented text
    const mockResponse = {
      auditory_output: {
        tts_engine: "gTTS (fallback)",
        segments: 2,
        available_voices: {
          voices: [{ voice_id: "gtts", name: "Google TTS" }],
          fallback: true
        }
      },
      sensory_output: {
        haptic_pattern: {
          name: "text_generated",
          events: [
            { time: 0, intensity: 0.4, duration: 100 }
          ]
        },
        haptic_events_count: 1
      },
      knowledge_graph: {
        segments: [
          { text: "First segment.", index: 0, type: "sentence_group" }
        ],
        text_length: 15,
        processing_strategy: "adaptive"
      }
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<App />);

    const textarea = screen.getByPlaceholderText('在這裡輸入您的故事或情境...');
    const submitButton = screen.getByText('生成沉浸式體驗');

    // Enter text and submit
    fireEvent.change(textarea, { target: { value: 'Test text. More text.' } });
    fireEvent.click(submitButton);

    // Wait for results to appear
    await waitFor(() => {
      expect(screen.getByText('生成結果')).toBeInTheDocument();
    });

    // Check that segmentation info is displayed
    await waitFor(() => {
      const resultText = screen.getByText(/聽覺輸出/).parentElement.textContent;
      expect(resultText).toContain('segments');
    });
  });

  it('應該顯示觸覺反饋模式資訊', async () => {
    const mockResponse = {
      auditory_output: {
        tts_engine: "gTTS (fallback)",
        segments: 1
      },
      sensory_output: {
        haptic_pattern: {
          name: "text_generated",
          description: "Generated from text",
          events: [
            { time: 0, intensity: 0.9, duration: 80 },
            { time: 120, intensity: 0.6, duration: 120 }
          ],
          repeat: false
        },
        haptic_events_count: 2
      },
      knowledge_graph: {
        segments: [],
        text_length: 20
      }
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<App />);

    const textarea = screen.getByPlaceholderText('在這裡輸入您的故事或情境...');
    const submitButton = screen.getByText('生成沉浸式體驗');

    fireEvent.change(textarea, { target: { value: 'Hello! How are you?' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('生成結果')).toBeInTheDocument();
    });

    // Check that haptic pattern is displayed
    await waitFor(() => {
      const sensorText = screen.getByText(/感官輸出/).parentElement.textContent;
      expect(sensorText).toContain('haptic_pattern');
      expect(sensorText).toContain('haptic_events_count');
    });
  });

  it('應該正確處理 TTS 請求', async () => {
    const mockBlob = new Blob(['audio data'], { type: 'audio/mpeg' });
    
    global.fetch.mockResolvedValueOnce({
      ok: true,
      blob: async () => mockBlob,
    });

    // Mock URL.createObjectURL
    const mockUrl = 'blob:http://localhost/audio';
    global.URL.createObjectURL = vi.fn(() => mockUrl);

    render(<App />);

    const textarea = screen.getByPlaceholderText('在這裡輸入您的故事或情境...');
    const ttsButton = screen.getByText('播放語音');

    fireEvent.change(textarea, { target: { value: 'Test audio text' } });
    fireEvent.click(ttsButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tts'),
        expect.objectContaining({
          method: 'POST',
          body: expect.stringContaining('Test audio text')
        })
      );
    });

    // Check that audio player appears
    await waitFor(() => {
      const audioElement = screen.getByText(/語音輸出/);
      expect(audioElement).toBeInTheDocument();
    });
  });

  it('應該處理空文本輸入', async () => {
    render(<App />);

    const submitButton = screen.getByText('生成沉浸式體驗');
    fireEvent.click(submitButton);

    await waitFor(() => {
      // Error message now uses i18n placeholder text
      expect(screen.getByText('在這裡輸入您的故事或情境...')).toBeInTheDocument();
    });
  });

  it('應該處理 API 錯誤', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    render(<App />);

    const textarea = screen.getByPlaceholderText('在這裡輸入您的故事或情境...');
    const submitButton = screen.getByText('生成沉浸式體驗');

    fireEvent.change(textarea, { target: { value: 'Test text' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      // Error message now uses i18n format
      expect(screen.getByText(/API error/)).toBeInTheDocument();
    });
  });

  it('應該顯示文本長度和處理策略', async () => {
    const mockResponse = {
      auditory_output: {
        tts_engine: "gTTS (fallback)",
        segments: 3
      },
      sensory_output: {
        haptic_pattern: { name: "test", events: [] },
        haptic_events_count: 0
      },
      knowledge_graph: {
        segments: [
          { text: "Segment 1", index: 0 },
          { text: "Segment 2", index: 1 }
        ],
        text_length: 150,
        processing_strategy: "paragraphs"
      }
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<App />);

    const textarea = screen.getByPlaceholderText('在這裡輸入您的故事或情境...');
    const submitButton = screen.getByText('生成沉浸式體驗');

    fireEvent.change(textarea, { target: { value: 'Long text with multiple paragraphs.' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('生成結果')).toBeInTheDocument();
    });

    // Check that knowledge graph contains processing info
    await waitFor(() => {
      const kgText = screen.getByText(/知識圖譜/).parentElement.textContent;
      expect(kgText).toContain('processing_strategy');
      expect(kgText).toContain('text_length');
    });
  });
});
