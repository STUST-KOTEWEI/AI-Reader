export default function ProgressSection() {
  return (
    <section id="progress" className="py-16 md:py-24">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h3 className="text-3xl md:text-4xl font-bold">開發進度與原型</h3>
          <p className="mt-4 text-lg text-gray-600">
            我們已在Hugging Face平台部署了兩款原型，以驗證核心功能。
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* my-reader-gpt */}
          <div className="subtle-bg p-8 rounded-lg card-shadow">
            <h4 className="text-2xl font-bold mb-2">1. my-reader-gpt</h4>
            <span className="inline-block bg-blue-100 text-blue-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded">
              聲音核心測試版
            </span>
            <p className="mt-4 text-gray-600">
              此版本專注於將文字轉化為高品質、聽感自然的語音。我們成功解決了長篇文本生成中的韻律與一致性問題，為後續開發奠定了穩固基石。
            </p>
            <div className="mt-6">
              <p className="font-bold text-gray-700">語音自然度(MOS)評分:</p>
              <div className="chart-container">
                <MOSChart />
              </div>
            </div>
          </div>

          {/* holo-reader-final */}
          <div className="subtle-bg p-8 rounded-lg card-shadow">
            <h4 className="text-2xl font-bold mb-2">2. holo-reader-final</h4>
            <span className="inline-block bg-green-100 text-green-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded">
              多感官整合測試版
            </span>
            <img
              src="https://placehold.co/600x300/f5f1e8/586e75?text=Multi-Sensory+Signal+Mapping"
              alt="多感官訊號映射示意圖"
              className="rounded-md my-4 w-full object-cover"
            />
            <p className="mt-4 text-gray-600">
              作為更進階的版本，此原型開始整合多模態訊號映射。我們正聚焦於建立一套演算法，將文本中抽象的情緒（如懸疑、喜悅）有效轉譯為具體的觸覺、嗅覺等非視覺訊號。
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

// Simple MOS Chart using CSS bars (no Chart.js dependency)
function MOSChart() {
  const mosScore = 4.3;
  const maxScore = 5;
  const percentage = (mosScore / maxScore) * 100;

  return (
    <div className="mt-4">
      <div className="flex items-center gap-4">
        <div className="flex-1 bg-gray-200 rounded-full h-8 overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-1000"
            style={{
              width: `${percentage}%`,
              backgroundColor: 'rgba(38, 139, 210, 0.8)',
            }}
          />
        </div>
        <span className="font-bold text-lg" style={{ color: '#268bd2' }}>
          {mosScore.toFixed(1)} / {maxScore}.0
        </span>
      </div>
      <p className="text-xs text-gray-500 mt-2 text-center">
        MOS (平均意見分數) - 分數越高越好
      </p>
    </div>
  );
}
