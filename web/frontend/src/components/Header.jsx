import { useState } from 'react';

const sections = [
  { id: 'hero', label: '首頁' },
  { id: 'vision', label: '專案願景' },
  { id: 'scenarios', label: '應用情境' },
  { id: 'demo', label: '線上原型' },
  { id: 'engine', label: 'HSP引擎' },
  { id: 'progress', label: '開發進度' },
  { id: 'future', label: '未來展望' },
];

export default function Header() {
  const [mobileNavValue, setMobileNavValue] = useState('#hero');

  const handleScroll = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="accent-bg text-white p-4 sticky top-0 z-50 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl md:text-2xl font-bold">AI多感官智能閱讀器</h1>
        
        {/* Desktop Navigation */}
        <nav className="hidden md:flex space-x-6 font-medium">
          {sections.slice(1).map((section) => (
            <button
              key={section.id}
              onClick={() => handleScroll(section.id)}
              className="hover:text-gray-200 bg-transparent border-none text-white cursor-pointer"
            >
              {section.label}
            </button>
          ))}
        </nav>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <select
            value={mobileNavValue}
            onChange={(e) => {
              setMobileNavValue(e.target.value);
              handleScroll(e.target.value.replace('#', ''));
            }}
            className="bg-white text-gray-800 rounded p-2"
          >
            {sections.map((section) => (
              <option key={section.id} value={`#${section.id}`}>
                {section.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
