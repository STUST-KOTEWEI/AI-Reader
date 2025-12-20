import { useState, useEffect } from 'react';
import './App.css';

// Import components
import Header from './components/Header';
import ApiKeySheet from './components/ApiKeySheet';
import HeroSection from './components/HeroSection';
import VisionSection from './components/VisionSection';
import ScenariosSection from './components/ScenariosSection';
import InteractiveDemo from './components/InteractiveDemo';
import EngineSection from './components/EngineSection';
import ProgressSection from './components/ProgressSection';
import FutureSection from './components/FutureSection';
import Footer from './components/Footer';

function App() {
  const [showApiKeySheet, setShowApiKeySheet] = useState(false);

  // Check if API key exists on mount
  useEffect(() => {
    const hasKey = localStorage.getItem('GEMINI_API_KEY');
    if (!hasKey) {
      setShowApiKeySheet(true);
    }
  }, []);

  return (
    <div className="App antialiased">
      {/* API Key Settings Button */}
      <button
        onClick={() => setShowApiKeySheet(true)}
        className="fixed bottom-4 right-4 z-40 rounded-full bg-blue-600 text-white w-12 h-12 shadow-lg cursor-pointer border-none"
        aria-label="設定 API Key"
      >
        ⚙️
      </button>

      {/* API Key Sheet */}
      <ApiKeySheet
        isOpen={showApiKeySheet}
        onClose={() => setShowApiKeySheet(false)}
      />

      {/* Header */}
      <Header />

      {/* Main Content */}
      <main>
        <HeroSection />
        <VisionSection />
        <ScenariosSection />
        <InteractiveDemo onOpenApiKeySheet={() => setShowApiKeySheet(true)} />
        <EngineSection />
        <ProgressSection />
        <FutureSection />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
