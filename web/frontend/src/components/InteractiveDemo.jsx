import { useState, useRef, useEffect } from 'react';

// API URL - use environment variable or default to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Voice language options
const voiceLanguages = [
  '中文', '英文', '日文', 'ar-EG', 'de-DE', 'en-US', 'es-US', 'fr-FR', 
  'hi-IN', 'id-ID', 'it-IT', 'ja-JP', 'ko-KR', 'pt-BR', 'ru-RU', 
  'nl-NL', 'pl-PL', 'th-TH', 'tr-TR', 'vi-VN', 'ro-RO', 'uk-UA', 
  'bn-BD', 'en-IN', 'mr-IN', 'ta-IN', 'te-IN'
];

// Style sensors configuration
const styleSensors = [
  { style: '溫暖且引人入勝', icon: '🖐️', title: '手環：偵測到平靜的心率' },
  { style: '生動活潑的故事風格', icon: '📷', title: '鏡頭：偵測到微笑表情' },
  { style: '專業且清晰', icon: '👓', title: '智慧眼鏡：偵測到閱讀專注模式' },
];

/**
 * Decodes a base64-encoded string to an ArrayBuffer
 * @param {string} base64 - The base64-encoded string to decode
 * @returns {ArrayBuffer} The decoded binary data as an ArrayBuffer
 */
function base64ToArrayBuffer(base64) {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Converts raw PCM audio data to WAV format
 * @param {Int16Array} pcmData - Raw 16-bit PCM audio samples
 * @param {number} sampleRate - Sample rate of the audio (e.g., 22050, 44100)
 * @returns {Blob} A Blob containing the WAV file data
 * 
 * WAV file structure:
 * - RIFF header (12 bytes)
 * - fmt chunk (24 bytes) - format information
 * - data chunk (8 bytes + audio data) - raw PCM samples
 */
function pcmToWav(pcmData, sampleRate) {
  const numChannels = 1;
  const bitsPerSample = 16;
  const byteRate = sampleRate * numChannels * bitsPerSample / 8;
  const blockAlign = numChannels * bitsPerSample / 8;
  const dataSize = pcmData.length * pcmData.BYTES_PER_ELEMENT;
  
  const buffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buffer);

  function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }

  // RIFF header
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + dataSize, true);
  writeString(view, 8, 'WAVE');
  // fmt chunk
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, byteRate, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, bitsPerSample, true);
  // data chunk
  writeString(view, 36, 'data');
  view.setUint32(40, dataSize, true);

  // Write PCM data
  const pcm = new Int16Array(pcmData);
  for (let i = 0; i < pcm.length; i++) {
    view.setInt16(44 + i * 2, pcm[i], true);
  }

  return new Blob([view], { type: 'audio/wav' });
}

export default function InteractiveDemo({ onOpenApiKeySheet }) {
  // State
  const [activeTab, setActiveTab] = useState('demo-text');
  const [text, setText] = useState('');
  const [selectedLang, setSelectedLang] = useState('中文');
  const [selectedStyle, setSelectedStyle] = useState('溫暖且引人入勝');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [audioUrl, setAudioUrl] = useState('');
  const [generateButtonText, setGenerateButtonText] = useState('🚀 開始生成完整體驗');

  // Camera states
  const [showCamera, setShowCamera] = useState(false);
  const [imagePreview, setImagePreview] = useState('');
  const [imageCaption, setImageCaption] = useState('');
  const [showFaceCamera, setShowFaceCamera] = useState(false);
  const [emotionResult, setEmotionResult] = useState('');

  // Refs
  const cameraStreamRef = useRef(null);
  const videoRef = useRef(null);
  const faceVideoRef = useRef(null);
  const currentStreamRef = useRef(null);

  // Cleanup camera on unmount
  useEffect(() => {
    return () => {
      if (currentStreamRef.current) {
        currentStreamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const stopCameraStream = () => {
    if (currentStreamRef.current) {
      currentStreamRef.current.getTracks().forEach(track => track.stop());
      currentStreamRef.current = null;
    }
  };

  // Book cover / ISBN camera logic
  const handleTakePhoto = async () => {
    setShowCamera(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      currentStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      setError('無法啟動相機。請確認權限。');
      setShowCamera(false);
    }
  };

  const handleCapture = () => {
    if (!videoRef.current) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
    const imageUrl = canvas.toDataURL('image/jpeg');
    
    setImagePreview(imageUrl);
    stopCameraStream();
    setShowCamera(false);

    setImageCaption('正在辨識拍攝的書籍...');
    setTimeout(() => {
      const simulatedText = '偵測到拍攝書籍：《人類大歷史》。這本書從十萬年前有生命跡象開始，講述了人類如何崛起成為地球的主宰...';
      setImageCaption('辨識完成！');
      setText(simulatedText);
    }, 1500);
  };

  const handleCancelCamera = () => {
    stopCameraStream();
    setShowCamera(false);
  };

  const handleImageUpload = (event) => {
    if (event.target.files?.[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
        setText('');
        setResult(null);
        setImageCaption('正在辨識書籍封面/ISBN...');
        setTimeout(() => {
          const isISBN = Math.random() > 0.5;
          const simulatedText = isISBN
            ? '偵測到 ISBN 條碼。書名：《三體》，作者：劉慈欣。這是一部描繪宇宙文明間生存鬥爭的科幻史詩...'
            : '偵測到書籍封面：《小王子》。這本書透過一位來自外星球的小王子的視角，探討了愛、失落與人生的真諦...';
          setImageCaption(isISBN ? 'ISBN 辨識完成！' : '封面辨識完成！');
          setText(simulatedText);
        }, 1500);
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  };

  // Face recognition logic
  const handleFaceRecognition = async () => {
    setEmotionResult('正在啟動鏡頭並分析情緒...');
    setShowFaceCamera(true);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      currentStreamRef.current = stream;
      if (faceVideoRef.current) {
        faceVideoRef.current.srcObject = stream;
      }

      const emotions = [
        { emotion: '開心 😊', text: '今天真是個好日子，陽光普照，微風徐徐...' },
        { emotion: '平靜 😌', text: '寧靜的午後，適合來杯茶，靜靜地看本書。' },
        { emotion: '驚訝 😮', text: '哇！真是個意想不到的發展，接下來會發生什麼事呢？' },
        { emotion: '專注 🤔', text: '讓我們來深入探討這個複雜的問題，抽絲剝繭找出答案。' },
      ];
      const detected = emotions[Math.floor(Math.random() * emotions.length)];
      
      setTimeout(() => {
        setEmotionResult('偵測到情緒：' + detected.emotion);
        setText(detected.text);
      }, 2000);
    } catch (err) {
      setEmotionResult('無法啟動鏡頭。');
      setShowFaceCamera(false);
    }
  };

  // Generate experience - calls backend API
  const handleGenerate = async () => {
    if (!text.trim()) {
      setError('請先輸入文字、上傳圖片或進行臉部辨識');
      return;
    }

    setError('');
    setAudioUrl('');
    setResult(null);
    setLoading(true);
    setGenerateButtonText('✨ AI分析情境中...');

    try {
      // Call backend API for immersion generation
      const response = await fetch(`${API_URL}/generate_immersion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`API 請求失敗，狀態碼: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);

      // Add sensory feedback animation
      document.body.classList.add('sensory-feedback');
      setTimeout(() => document.body.classList.remove('sensory-feedback'), 300);

      // Generate TTS
      setGenerateButtonText('✨ 高品質語音生成中...');
      
      const ttsResponse = await fetch(`${API_URL}/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, lang: selectedLang === '中文' ? 'zh-tw' : 'en' }),
      });

      if (ttsResponse.ok) {
        const blob = await ttsResponse.blob();
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
        setGenerateButtonText('正在播放...');
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setGenerateButtonText('🚀 開始生成完整體驗');
    }
  };

  const tabs = [
    { id: 'demo-text', label: '📝 文字輸入' },
    { id: 'demo-book', label: '📚 書籍封面/ISBN' },
    { id: 'demo-face', label: '😊 情感臉部辨識' },
  ];

  return (
    <section id="demo" className="py-16 md:py-24 bg-white">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h3 className="text-3xl md:text-4xl font-bold">線上原型互動</h3>
          <p className="mt-4 text-lg text-gray-600">
            親身體驗 Project-HOLO 的核心功能！選擇一種輸入方式，感受多模態的魅力。
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          {/* Tabs */}
          <div className="mb-4 border-b border-gray-200">
            <ul className="flex flex-wrap -mb-px text-sm font-medium text-center">
              {tabs.map((tab) => (
                <li key={tab.id} className="mr-2">
                  <button
                    onClick={() => setActiveTab(tab.id)}
                    className={`inline-block p-4 border-b-2 rounded-t-lg bg-transparent cursor-pointer ${
                      activeTab === tab.id
                        ? 'tab-active'
                        : 'border-transparent hover:text-gray-600 hover:border-gray-300'
                    }`}
                  >
                    {tab.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Tab Content */}
          <div className="demo-content">
            {/* Text Input Tab */}
            {activeTab === 'demo-text' && (
              <div className="flex flex-col gap-4">
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="在這裡輸入您的故事或情境... 例如：在一個下著雨的夜晚，我獨自走在森林裡..."
                  rows={5}
                  className="w-full p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 transition duration-200 resize-none subtle-bg"
                />
              </div>
            )}

            {/* Book/ISBN Tab */}
            {activeTab === 'demo-book' && (
              <div className="flex flex-col gap-4">
                {!showCamera && !imagePreview && (
                  <div className="flex gap-4">
                    <label className="flex-1 flex flex-col items-center justify-center w-full p-4 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                      <svg className="w-8 h-8 mb-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                      </svg>
                      <span className="font-semibold text-sm">從檔案上傳</span>
                      <input 
                        type="file" 
                        className="hidden" 
                        accept="image/*"
                        onChange={handleImageUpload}
                      />
                    </label>
                    <button
                      onClick={handleTakePhoto}
                      className="flex-1 flex flex-col items-center justify-center w-full p-4 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
                    >
                      <svg className="w-8 h-8 mb-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <span className="font-semibold text-sm">使用相機拍照</span>
                    </button>
                  </div>
                )}

                {showCamera && (
                  <div className="w-full aspect-video bg-gray-900 rounded-lg relative">
                    <video
                      ref={videoRef}
                      className="w-full h-full rounded-lg"
                      autoPlay
                      playsInline
                    />
                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-4">
                      <button
                        onClick={handleCapture}
                        className="w-16 h-16 bg-white rounded-full border-4 border-gray-400 focus:outline-none"
                      />
                      <button
                        onClick={handleCancelCamera}
                        className="text-white bg-red-600 rounded-full w-8 h-8 flex items-center justify-center"
                      >
                        X
                      </button>
                    </div>
                  </div>
                )}

                {imagePreview && (
                  <div className="w-full text-center">
                    <img
                      src={imagePreview}
                      alt="Image preview"
                      className="max-h-60 mx-auto rounded-lg shadow-md"
                    />
                    <p className="text-sm text-gray-600 mt-2">{imageCaption}</p>
                    <button
                      onClick={() => {
                        setImagePreview('');
                        setImageCaption('');
                      }}
                      className="mt-2 text-sm text-blue-600 hover:underline bg-transparent border-none cursor-pointer"
                    >
                      重新上傳
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Face Recognition Tab */}
            {activeTab === 'demo-face' && (
              <div className="flex flex-col gap-4">
                <div className="w-full bg-gray-900 aspect-video rounded-lg flex items-center justify-center text-white mb-4 relative">
                  {showFaceCamera ? (
                    <video
                      ref={faceVideoRef}
                      className="w-full h-full rounded-lg"
                      autoPlay
                      playsInline
                    />
                  ) : (
                    <img
                      src="https://storage.googleapis.com/be-prod-data-gcs-models-and-assets-v2/image_b1d420.png"
                      alt="鏡頭未啟動"
                      className="w-full h-full object-cover rounded-lg"
                    />
                  )}
                </div>
                <button
                  onClick={handleFaceRecognition}
                  className="w-full bg-purple-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-purple-700 transition duration-200 cursor-pointer"
                >
                  啟動鏡頭並辨識情緒
                </button>
                <p className="text-center mt-2 font-medium h-6">{emotionResult}</p>
              </div>
            )}
          </div>

          {/* Voice Language & Style Selection */}
          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                選擇或輸入語言
              </label>
              <input
                list="voice-lang-list"
                value={selectedLang}
                onChange={(e) => setSelectedLang(e.target.value)}
                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border"
              />
              <datalist id="voice-lang-list">
                {voiceLanguages.map((lang) => (
                  <option key={lang} value={lang} />
                ))}
              </datalist>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                聲音風格 (由感測器模擬)
              </label>
              <div className="mt-1 flex justify-around p-2 bg-gray-100 rounded-md">
                {styleSensors.map((sensor) => (
                  <button
                    key={sensor.style}
                    onClick={() => setSelectedStyle(sensor.style)}
                    className={`style-sensor ${selectedStyle === sensor.style ? 'active' : ''}`}
                    title={sensor.title}
                  >
                    {sensor.icon}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Generate Button */}
          <div className="flex flex-col sm:flex-row gap-4 mt-6">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-500 to-green-500 text-white font-bold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-green-600 transition duration-200 disabled:opacity-50 cursor-pointer"
            >
              {loading && <span className="loader" />}
              <span>{generateButtonText}</span>
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="text-red-600 mt-4 text-center">{error}</div>
          )}

          {/* Audio Player */}
          <div className="audio-player-container mt-6 w-full">
            {audioUrl ? (
              <audio controls autoPlay src={audioUrl} className="w-full">
                您的瀏覽器不支援音訊播放。
              </audio>
            ) : (
              <p className="text-center text-gray-500 text-sm">
                語音播放器將會顯示於此。
              </p>
            )}
          </div>

          {/* Results */}
          {result && (
            <div className="result-container mt-8 text-left card-shadow">
              <h2 className="text-2xl font-bold mb-4 border-b pb-2">✨ AI 生成結果</h2>
              <div className="result-section">
                <h3 className="font-bold text-lg accent-text">🎧 聽覺輸出建議</h3>
                <pre className="mt-2">
                  {JSON.stringify(result.auditory_output, null, 2)}
                </pre>
              </div>
              <div className="result-section mt-4">
                <h3 className="font-bold text-lg secondary-accent-text">🖐️ 感官輸出建議</h3>
                <pre className="mt-2">
                  {JSON.stringify(result.sensory_output, null, 2)}
                </pre>
              </div>
              <div className="result-section mt-4">
                <h3 className="font-bold text-lg text-purple-600">🧠 知識圖譜分析</h3>
                <pre className="mt-2">
                  {JSON.stringify(result.knowledge_graph, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
