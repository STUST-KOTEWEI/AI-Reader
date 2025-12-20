export default function VisionSection() {
  return (
    <section id="vision" className="py-16 md:py-24">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h3 className="text-3xl md:text-4xl font-bold">專案願景</h3>
          <p className="mt-4 text-lg text-gray-600">
            我們的核心理念是將科技與人性結合，解決傳統閱讀的限制。
          </p>
        </div>
        <div className="grid md:grid-cols-2 gap-8 md:gap-12">
          <div className="subtle-bg p-8 rounded-lg card-shadow">
            <div className="text-5xl accent-text mb-4">🌍</div>
            <h4 className="text-2xl font-bold mb-2">知識面前，人人平等</h4>
            <p className="text-gray-600">
              我們致力於打造一個無障礙的知識環境。無論是視障者、行動不便者，或是因語言文化隔閡而學習受阻的族群，都能透過多感官的互動方式，輕鬆獲取資訊與知識。
            </p>
          </div>
          <div className="subtle-bg p-8 rounded-lg card-shadow">
            <div className="text-5xl secondary-accent-text mb-4">🤝</div>
            <h4 className="text-2xl font-bold mb-2">讓科技暖起來</h4>
            <p className="text-gray-600">
              我們追求的不只是高效的資訊傳遞，更是一種有溫度的情感交流。目標是將人機互動從「工具」關係昇華為「夥伴」關係，讓科技成為促進心理健康、提供情感支持的溫暖媒介。
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
