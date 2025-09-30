import React from 'react';
import './App.css';
import Header from './components/Header';
import Hero from './components/Hero';
import SearchForm from './components/SearchForm';
import ActionButtons from './components/ActionButtons';

function App() {
  return (
    <div className="app">
      <div className="container">
        <Header />
        <main className="main">
          <Hero />
          <SearchForm />
          <ActionButtons />
        </main>
      </div>
    </div>
  );
}

export default App;
