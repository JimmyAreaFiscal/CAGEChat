import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';
import '../styles/Home.css';
import logo from '../assets/CAGEChat.png';
const Home = () => (
  <div className="App home-page">
    <div className="home-card">
      <img src={logo} alt="CAGEChat" className="home-logo" />
      <h1 className="home-title">Bem-vindo ao CAGEChat!</h1>
      <p className="home-desc">
        Seu assistente para consultas de normas jurídicas! 
      </p>
      <div className="home-nav">
        <Link to="/chat" className="home-btn home-btn-chat">Ir para o Chat</Link>
        <Link to="/question-collector" className="home-btn home-btn-question">Ajude o projeto!</Link>
        <Link to="/about" className="home-btn home-btn-about">Sobre o projeto</Link>
      </div>
    </div>
  </div>
);

export default Home; 