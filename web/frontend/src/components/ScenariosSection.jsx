export default function ScenariosSection() {
  const scenarios = [
    {
      icon: '🚿',
      title: '沐浴中閱讀',
      description: '搭配防水語音裝置與觸覺背心，邊洗澡邊聽書，並透過震動提示重點，將零碎時間轉化為學習時光。',
      engineTab: 'output',
    },
    {
      icon: '🚇',
      title: '通勤中學習',
      description: '在吵雜的捷運上，戴上耳機和嗅覺模組。當讀到咖啡主題文章時，釋放的咖啡香氣能幫助您提升專注力與情境感。',
      engineTab: 'output',
    },
    {
      icon: '😔',
      title: '疲憊時陪伴',
      description: '當您感到情緒低落時，系統能透過語音或表情偵測您的狀態，自動切換為鼓勵的語調與正向內容，提供溫暖的陪伴。',
      engineTab: 'input',
    },
  ];

  const handleEngineLink = (tabId) => {
    const engineSection = document.getElementById('engine');
    if (engineSection) {
      engineSection.scrollIntoView({ behavior: 'smooth' });
      // Dispatch custom event to switch tab
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('switchEngineTab', { detail: tabId }));
      }, 500);
    }
  };

  return (
    <section id="scenarios" className="py-16 md:py-24 subtle-bg">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h3 className="text-3xl md:text-4xl font-bold">應用情境</h3>
          <p className="mt-4 text-lg text-gray-600">
            在您意想不到的時刻，也能沉浸在知識與故事的懷抱中。
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {scenarios.map((scenario, index) => (
            <div key={index} className="bg-white p-8 rounded-lg card-shadow text-center">
              <div className="text-5xl mb-4">{scenario.icon}</div>
              <h4 className="text-2xl font-bold mb-2">{scenario.title}</h4>
              <p className="text-gray-600">
                {scenario.description.split(/觸覺|嗅覺|語音或表情/).map((part, i, arr) => {
                  if (i < arr.length - 1) {
                    const keyword = scenario.description.match(/觸覺|嗅覺|語音或表情/g)?.[i];
                    return (
                      <span key={i}>
                        {part}
                        <button
                          onClick={() => handleEngineLink(scenario.engineTab)}
                          className="accent-text hover:underline bg-transparent border-none cursor-pointer p-0"
                        >
                          {keyword}
                        </button>
                      </span>
                    );
                  }
                  return <span key={i}>{part}</span>;
                })}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
