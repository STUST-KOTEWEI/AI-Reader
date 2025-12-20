import { useState, useEffect } from 'react';

export default function ApiKeySheet({ isOpen, onClose }) {
  const [apiKey, setApiKey] = useState('');

  useEffect(() => {
    const savedKey = localStorage.getItem('GEMINI_API_KEY');
    if (savedKey) {
      setApiKey(savedKey);
    }
  }, [isOpen]);

  const handleSave = () => {
    if (!apiKey.trim()) {
      alert('請輸入 API Key');
      return;
    }
    localStorage.setItem('GEMINI_API_KEY', apiKey.trim());
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="api-key-sheet">
      <div className="flex items-center justify-between">
        <h2 className="font-bold text-gray-800">設定 Gemini API Key</h2>
        <button
          onClick={onClose}
          className="text-gray-500 bg-transparent border-none cursor-pointer text-xl"
        >
          ✕
        </button>
      </div>
      <p className="text-sm text-gray-600 mt-1">
        僅儲存於本機（localStorage）。可隨時點右下角齒輪開啟。
      </p>
      <div className="mt-3 flex gap-2">
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="AIza..."
          className="flex-1 border rounded px-3 py-2"
        />
        <button
          onClick={handleSave}
          className="px-4 py-2 bg-blue-600 text-white rounded cursor-pointer"
        >
          儲存
        </button>
      </div>
    </div>
  );
}
