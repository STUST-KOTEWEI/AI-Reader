import { useState } from 'react';
import './App.css';
import UserProfile from './components/UserProfile';
import { t } from './i18n/translations';

// 後端 API 的網址
const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [audioSrc, setAudioSrc] = useState('');
  const [ttsLoading, setTtsLoading] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [language, setLanguage] = useState('zh-tw');

  const handleProfileChange = (profile) => {
    setUserProfile(profile);
    // Update language when profile changes
    if (profile?.preferences?.preferred_language) {
      setLanguage(profile.preferences.preferred_language);
    }
  };

  const handleTTS = async () => {
    if (!text.trim()) {
      setError(t(language, 'placeholder'));
      return;
    }
    setTtsLoading(true);
    setError('');
    setAudioSrc('');

    try {
        const response = await fetch(`${API_URL}/tts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, lang: language })
        });

        if (!response.ok) {
            throw new Error(`TTS API error: ${response.status}`);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setAudioSrc(url);
    } catch (err) {
        setError(err.message);
    } finally {
        setTtsLoading(false);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    if (!text.trim()) {
      setError(t(language, 'placeholder'));
      setLoading(false);
      return;
    }

    try {
      const requestBody = { text: text };
      // Include user profile in request if available
      if (userProfile) {
        requestBody.user_profile = userProfile;
      }
      
      const response = await fetch(`${API_URL}/generate_immersion`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>{t(language, 'appTitle')}</h1>
        <p>{t(language, 'appSubtitle')}</p>
        <button 
          className="profile-button" 
          onClick={() => setProfileOpen(true)}
          aria-label={t(language, 'settings')}
        >
          ⚙️ {t(language, 'settings')}
        </button>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="narrative-form">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={t(language, 'placeholder')}
            rows="5"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? t(language, 'generating') : t(language, 'generate')}
          </button>
          <button type="button" onClick={handleTTS} disabled={ttsLoading}>
            {ttsLoading ? t(language, 'generatingAudio') : t(language, 'playAudio')}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}

        {audioSrc && (
          <div className="audio-player">
            <h3>{t(language, 'audioOutput')}</h3>
            <audio controls autoPlay src={audioSrc}>
              {t(language, 'browserNotSupported')}
            </audio>
          </div>
        )}

        {result && (
          <div className="result-container">
            <h2>{t(language, 'results')}</h2>
            <div className="result-section">
              <h3>{t(language, 'auditoryOutput')}</h3>
              <pre>{JSON.stringify(result.auditory_output, null, 2)}</pre>
            </div>
            <div className="result-section">
              <h3>{t(language, 'sensoryOutput')}</h3>
              <pre>{JSON.stringify(result.sensory_output, null, 2)}</pre>
            </div>
            <div className="result-section">
              <h3>{t(language, 'knowledgeGraph')}</h3>
              <pre>{JSON.stringify(result.knowledge_graph, null, 2)}</pre>
            </div>
          </div>
        )}
      </main>

      <UserProfile
        isOpen={profileOpen}
        onClose={() => setProfileOpen(false)}
        onProfileChange={handleProfileChange}
        language={language}
      />
    </div>
  );
}

export default App;
