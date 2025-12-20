export default function HeroSection() {
  return (
    <section id="hero" className="py-20 md:py-32 text-center subtle-bg">
      <div className="container mx-auto px-6 flex flex-col items-center">
        <img
          src="https://placehold.co/900x400/0d1117/268bd2?text=Holo-Sentient+Engine"
          alt="AI感知引擎示意圖"
          className="rounded-lg shadow-2xl mb-12 w-full max-w-4xl"
        />
        <h2 className="text-4xl md:text-6xl font-bold accent-text mb-4">
          Holo-Sentient 感知引擎
        </h2>
        <p className="text-lg md:text-2xl text-gray-600 max-w-3xl mx-auto">
          讓知識與情感，在任何情境下都能被感知。我們正在打造一套超越視覺的AI閱讀器，開啟全新的人機互動篇章。
        </p>
      </div>
    </section>
  );
}
