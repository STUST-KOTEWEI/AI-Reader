import { useState, useEffect } from 'react';

export default function EngineSection() {
  const [activeTab, setActiveTab] = useState('input');

  // Listen for tab switch events from other components
  useEffect(() => {
    const handleTabSwitch = (event) => {
      setActiveTab(event.detail);
    };
    window.addEventListener('switchEngineTab', handleTabSwitch);
    return () => window.removeEventListener('switchEngineTab', handleTabSwitch);
  }, []);

  const tabs = [
    { id: 'input', label: '➡️ 輸入子系統' },
    { id: 'core', label: '⚙️ 核心處理引擎' },
    { id: 'output', label: '⬅️ 輸出子系統' },
  ];

  return (
    <section id="engine" className="py-16 md:py-24 subtle-bg">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h3 className="text-3xl md:text-4xl font-bold">HSP引擎互動詳解</h3>
          <p className="mt-4 text-lg text-gray-600">
            點擊下方模組，探索HSP引擎如何感知文字背後的情感與氛圍。
          </p>
        </div>

        <div className="flex flex-col md:flex-row gap-8">
          {/* Tab Buttons */}
          <div className="md:w-1/3">
            <div className="flex flex-col space-y-4">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`p-4 text-left text-lg border-l-4 rounded-r-md bg-white cursor-pointer ${
                    activeTab === tab.id
                      ? 'tab-active'
                      : 'border-transparent hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <div className="md:w-2/3 bg-white p-8 rounded-lg card-shadow">
            {activeTab === 'input' && <InputSubsystem />}
            {activeTab === 'core' && <CoreProcessing />}
            {activeTab === 'output' && <OutputSubsystem />}
          </div>
        </div>
      </div>
    </section>
  );
}

function InputSubsystem() {
  return (
    <div>
      <h4 className="text-2xl font-bold accent-text mb-4">輸入子系統 (Input Subsystems)</h4>
      <p className="mb-4 text-gray-600">
        這是HSP引擎感知世界的起點，它從多個維度接收資訊，不僅僅是文字。
      </p>
      <ul className="space-y-3 list-disc list-inside text-gray-700">
        <li><strong>文字解析：</strong> 讀懂您提供的文本、文章。</li>
        <li><strong>ISBN/封面辨識：</strong> 只需掃描書籍條碼或封面，即可快速取得書籍資訊並開始沉浸式閱讀。</li>
        <li><strong>影像與臉部辨識：</strong> 分析圖像內容或您的臉部表情，將視覺元素轉化為其他感官體驗。</li>
        <li><strong>語音辨識與韻律分析：</strong> 不只聽懂您說話的內容，更能分析您的語氣情感。</li>
        <li><strong>生物特徵感測：</strong> 連接智慧手錶等穿戴裝置，讀取心跳等生理訊號，了解您的即時情緒狀態。</li>
      </ul>
    </div>
  );
}

function CoreProcessing() {
  return (
    <div>
      <h4 className="text-2xl font-bold accent-text mb-4">核心處理：HSP引擎 (Core Processing)</h4>
      <p className="mb-4 text-gray-600">
        這裡是系統的心臟與大腦。它將接收到的資訊轉化為豐富的多感官訊號。
      </p>
      <ul className="space-y-3 list-disc list-inside text-gray-700">
        <li><strong>NLP & SQL 資料庫：</strong> 透過自然語言處理(NLP)分析使用者偏好，並將這些數據結構化存儲於SQL資料庫，形成個人化的感官設定檔。</li>
        <li><strong>LLM Fine-Tuning：</strong> 基於使用者的回饋與偏好資料，對大型語言模型(LLM)進行微調，讓生成的內容與感官建議更貼近個人風格。</li>
        <li><strong>情感回饋迴路：</strong> 偵測您的情緒，若您感到疲憊，系統會自動放慢語速或切換音色。</li>
        <li><strong>多模態訊號輸出：</strong> 根據文本情境，觸發氣味、震動等訊號，創造身歷其境的體驗。</li>
      </ul>
    </div>
  );
}

function OutputSubsystem() {
  const [showAnimation, setShowAnimation] = useState(false);

  useEffect(() => {
    setShowAnimation(true);
    const timer = setTimeout(() => setShowAnimation(false), 5000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div>
      <h4 className="text-2xl font-bold accent-text mb-4">輸出子系統 (Output Subsystems)</h4>
      <p className="mb-4 text-gray-600">
        將引擎處理後的結果，以最真實、最沉浸的方式呈現給您。
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="simulation-container">
          <h6 className="font-bold">觸覺回饋 (Haptic)</h6>
          <p className="text-xs text-gray-500">
            透過
            <a href="https://teslasuit.io/" target="_blank" rel="noreferrer" className="accent-text hover:underline">
              Teslasuit
            </a>
            等裝置，模擬心跳、雨滴等感覺。
          </p>
        </div>
        
        <div className={`simulation-container relative ${showAnimation ? 'aroma-active' : ''}`}>
          <h6 className="font-bold">嗅覺模擬 (Olfactory)</h6>
          <p className="text-xs text-gray-500">當偵測到關鍵字「咖啡」，釋放模擬香氣。</p>
          {showAnimation && (
            <div className="absolute bottom-0 left-0 w-full h-full pointer-events-none">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="aroma-particle"
                  style={{
                    left: `${40 + Math.random() * 20}%`,
                    animationDelay: `${Math.random() * 2}s`,
                  }}
                />
              ))}
            </div>
          )}
        </div>
        
        <div className="simulation-container">
          <h6 className="font-bold">味覺模擬 (Gustatory)</h6>
          <p className="text-xs text-gray-500">當偵測到關鍵字「甜」，觸發味覺裝置。</p>
          <p className={`text-center font-bold secondary-accent-text mt-4 transition-opacity ${showAnimation ? 'opacity-100' : 'opacity-0'}`}>
            釋放「甜味」訊號...
          </p>
        </div>
      </div>

      <h5 className="text-xl font-bold text-gray-800 mt-8 mb-3">前瞻性輸出：視覺與物理互動</h5>
      <p className="mb-4 text-gray-600">
        我們的終極目標是模糊現實與故事的界線。系統會參照您的臉部表情與閱讀內容，動態生成視覺與物理輸出：
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="text-center">
          <h6 className="font-bold">模擬：互動動態投影</h6>
          <p className="text-xs text-gray-500 mb-2">偵測到「開心」情緒時</p>
          <div className={`projection-cup ${showAnimation ? 'projection-happy' : ''}`}>
            <div className="projection-overlay">✨</div>
          </div>
        </div>
        
        <div className="text-center">
          <h6 className="font-bold">模擬：可編程物質</h6>
          <p className="text-xs text-gray-500 mb-2">偵測到「平靜」與「驚訝」情緒時</p>
          <ProgrammableMatterGrid showAnimation={showAnimation} />
        </div>
      </div>

      <div className="relative rounded-lg overflow-hidden shadow-lg" style={{ paddingTop: '56.25%' }}>
        <iframe
          className="absolute top-0 left-0 w-full h-full"
          src="https://www.youtube.com/embed/5B-hyodzi1w"
          title="YouTube video player"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
        />
      </div>
      <p className="text-xs text-center mt-2 text-gray-500">
        影片來源: MIT CSAIL - Interactive Dynamic Video
      </p>
    </div>
  );
}

function ProgrammableMatterGrid({ showAnimation }) {
  const [phase, setPhase] = useState('normal');

  useEffect(() => {
    if (showAnimation) {
      const timer1 = setTimeout(() => setPhase('calm'), 500);
      const timer2 = setTimeout(() => setPhase('excited'), 2500);
      const timer3 = setTimeout(() => setPhase('normal'), 4500);
      return () => {
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    }
  }, [showAnimation]);

  return (
    <div className={`pm-grid ${phase === 'calm' ? 'pm-calm' : phase === 'excited' ? 'pm-excited' : ''}`}>
      {[...Array(100)].map((_, i) => (
        <div key={i} className="pm-cell" />
      ))}
    </div>
  );
}
