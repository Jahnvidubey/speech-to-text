// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import UploadAndList from './UploadAndList';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Audio Transcription App</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<UploadAndList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
