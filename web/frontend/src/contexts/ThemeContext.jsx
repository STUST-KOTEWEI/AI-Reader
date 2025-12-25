import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const themes = {
  dark: {
    name: 'dark',
    colors: {
      primary: '#845ef7',
      secondary: '#ff6b9d',
      background: 'linear-gradient(135deg, #0f0a1f, #1a0f2e)',
      surface: 'rgba(30, 15, 60, 0.95)',
      text: '#ffffff',
      textSecondary: 'rgba(255, 255, 255, 0.7)',
      border: 'rgba(255, 255, 255, 0.1)',
      error: '#ff6b9d',
      success: '#4ade80',
      warning: '#fbbf24'
    }
  },
  light: {
    name: 'light',
    colors: {
      primary: '#6d28d9',
      secondary: '#ec4899',
      background: 'linear-gradient(135deg, #f8fafc, #e2e8f0)',
      surface: 'rgba(255, 255, 255, 0.95)',
      text: '#1e293b',
      textSecondary: 'rgba(30, 41, 59, 0.7)',
      border: 'rgba(0, 0, 0, 0.1)',
      error: '#ef4444',
      success: '#22c55e',
      warning: '#f59e0b'
    }
  },
  auto: {
    name: 'auto'
  }
};

export function ThemeProvider({ children }) {
  const [themeName, setThemeName] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved || 'dark';
  });
  
  const [resolvedTheme, setResolvedTheme] = useState(themes.dark);
  
  useEffect(() => {
    // Determine actual theme based on preference
    let actualTheme = themeName;
    
    if (themeName === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      actualTheme = prefersDark ? 'dark' : 'light';
    }
    
    setResolvedTheme(themes[actualTheme] || themes.dark);
    
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', actualTheme);
    localStorage.setItem('theme', themeName);
    
    // Apply CSS variables
    const theme = themes[actualTheme] || themes.dark;
    const root = document.documentElement;
    
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value);
    });
    
  }, [themeName]);
  
  // Listen for system theme changes when in auto mode
  useEffect(() => {
    if (themeName !== 'auto') return;
    
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      const actualTheme = e.matches ? 'dark' : 'light';
      setResolvedTheme(themes[actualTheme]);
      document.documentElement.setAttribute('data-theme', actualTheme);
    };
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [themeName]);
  
  const setTheme = (name) => {
    if (themes[name] || name === 'auto') {
      setThemeName(name);
    }
  };
  
  const toggleTheme = () => {
    setThemeName(current => {
      if (current === 'dark') return 'light';
      if (current === 'light') return 'auto';
      return 'dark';
    });
  };
  
  return (
    <ThemeContext.Provider value={{
      theme: resolvedTheme,
      themeName,
      setTheme,
      toggleTheme,
      isDark: resolvedTheme.name === 'dark'
    }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

export default ThemeContext;
