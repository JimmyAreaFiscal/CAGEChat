import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/CAGEChat.png';
import plusIcon from '../assets/add-30.png';
import '../styles/Sidebar.css';

const homeIcon = require('../assets/home.svg');
const savedIcon = require('../assets/bookmark.svg');
const rocketIcon = require('../assets/rocket.svg');

const Sidebar = ({ functionToCallForPreviousId, stringToShow="Novo Chat", listOfTabs=[{name: "Conversa Atual", checkpointer_id: 0}, {name: "Conversa 2", checkpointer_id: 1}, {name: "Conversa 3", checkpointer_id: 2}], functionToCallForAddButton }) => (
  
  <aside className="sidemenu">
    <div className='side-menu-header'>
      <img src={logo} alt="Cage Chat" />
      <h1>CAGEChat</h1>
      <p>Seu assistente de conhecimento</p>
    </div>
    
    <div className='sidemenu-tabs-container'>
      {stringToShow && (
        <div className="side-menu-button" onClick={() => functionToCallForAddButton()}>
          <img src={plusIcon} alt={stringToShow} className='side-menu-add-button-icon'/>
          {stringToShow}
        </div>
      )}

      <div className='tabs-container'>
        {listOfTabs.map((tab, index) => (
            <div
              key={index}
              className="side-menu-button"
              onClick={() => functionToCallForPreviousId(null, tab.checkpointer_id)}
            >
              {tab.name}
            </div> 
        ))}
      </div>
    </div>
    <nav className="sidemenu-router-nav">
      <Link to="/" className="sidemenu-router-link">Home</Link>
      <Link to="/chat" className="sidemenu-router-link">Chat</Link>
      <Link to="/question-collector" className="sidemenu-router-link">Ajude o projeto</Link>
      <Link to="/about" className="sidemenu-router-link">Sobre o projeto</Link>
    </nav>

    <div className='sidemenu-footer'>
      <p>CAGEChat</p>
      <p>Versão 1.0</p>
      <p>Github - <a href="https://github.com/JimmyAreaFiscal/CAGEChat" target="_blank" rel="noopener noreferrer">JimmyAreaFiscal:CAGEChat</a></p>
    </div>
    
  </aside>
);

export default Sidebar; 