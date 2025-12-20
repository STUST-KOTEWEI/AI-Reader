import { useState } from 'react';

const futureVisions = [
  {
    icon: '🧠',
    title: '腦波直接讀取',
    description: '整合EEG技術，直接從腦波判斷您的專注與放鬆狀態，實現毫秒級的互動反應。',
  },
  {
    icon: '🎯',
    title: '情境感知推薦',
    description: '不僅根據您的偏好，更能結合當下心境推薦內容。心情不好時，為您送上溫暖的故事。',
  },
  {
    icon: '✍️',
    title: '創作者生態系',
    description: '提供工具，讓作家能為作品嵌入「感官特效」，催生全新的互動式內容創作。',
  },
  {
    icon: '🧊',
    title: '可編程物質',
    description: '將故事「召喚」到現實！讓您親手觸摸到書中描寫的山丘或動物的質感。',
  },
  {
    icon: '✨',
    title: '互動動態投影',
    description: '將動畫投影到日常物品上，讓您桌上的馬克杯冒出書中描寫的熱氣，模糊現實與故事的界線。',
  },
  {
    icon: '🔋',
    title: '次世代能源',
    description: '導入微型核電池或量子充電技術，實現真正的無線自由，讓裝置永遠陪伴在您身邊。',
  },
];

export default function FutureSection() {
  const [selectedCards, setSelectedCards] = useState(new Set());

  const toggleCard = (index) => {
    const newSelected = new Set(selectedCards);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelectedCards(newSelected);
  };

  return (
    <section id="future" className="py-16 md:py-24 subtle-bg">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h3 className="text-3xl md:text-4xl font-bold">未來展望</h3>
          <p className="mt-4 text-lg text-gray-600">
            我們的終極夢想是打造一個真正懂您的AI閱讀夥伴，以下是我們想挑戰的瘋狂點子！
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {futureVisions.map((vision, index) => (
            <div
              key={index}
              onClick={() => toggleCard(index)}
              className={`future-card bg-white p-6 rounded-lg card-shadow text-center relative ${
                selectedCards.has(index) ? 'opacity-50' : ''
              }`}
            >
              {selectedCards.has(index) && (
                <div className="absolute top-2 right-2 bg-green-500 rounded-full w-6 h-6 flex items-center justify-center">
                  <svg
                    className="w-4 h-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={3}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
              )}
              <div className="text-4xl mb-3">{vision.icon}</div>
              <h5 className="text-xl font-bold">{vision.title}</h5>
              <p className="text-sm text-gray-600 mt-2">{vision.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
