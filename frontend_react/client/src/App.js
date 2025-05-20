// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ChatPage from './pages/ChatPage';
import QuestionCollector from './pages/QuestionCollector';
import QuestionDetail from './pages/QuestionDetail';
import AboutProject from './pages/AboutProject';
import './App.css';
import './normal.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/question-collector" element={<QuestionCollector />} />
        <Route path="/question/:id" element={<QuestionDetail />} />
        <Route path="/about" element={<AboutProject />} />
      </Routes>
    </Router>
  );
}

export default App;
