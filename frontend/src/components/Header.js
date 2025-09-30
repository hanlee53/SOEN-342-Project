import React, { useState, useEffect } from 'react';

function Header() {
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  useEffect(() => {
    // Apply theme to document body
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
      document.body.classList.remove('light-mode');
    } else {
      document.body.classList.add('light-mode');
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="train-icon">🚂</span>
          <span className="logo-text">RailConnect</span>
        </div>
        <div className="header-actions">
          <button className="theme-toggle" onClick={toggleTheme}>
            {isDarkMode ? '🌙' : '☀️'}
          </button>
          <button className="menu-btn">☰</button>
        </div>
      </div>
    </header>
  );
}

export default Header;
