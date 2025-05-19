// App.js
import React, { useState } from 'react';
import './App.css';
import './normal.css';
import { chatStream } from './components/request_chat';
import { useRef } from 'react';


function App() {

  const [checkpointId, setCheckpointId] = useState(null);
  const [input, setInput] = useState('');
  // Cada entry de chatLog agora tem um campo `thoughts: []`
  const [chatLog, setChatLog] = useState([
    { user: 'gpt', message: 'Olá, como posso ajudar você hoje?', type: 'final_answer', thoughts: [] }
  ]);
  // Guarda temporariamente todos os pensamentos antes de “flush” no final_answer
  const [pendingThoughts, setPendingThoughts] = useState([]);
  // Pensamento corrente para renderização temporária
  const [currentThought, setCurrentThought] = useState(null);
  // Pensamentos da mensagem selecionada para abrir no modal
  const [modalThoughts, setModalThoughts] = useState(null);
  
  const pendingRef = useRef([]);

  async function handleSubmit(e) {

    e.preventDefault();
    // 1) adiciona mensagem do usuário
    setChatLog(prev => [
      ...prev,
      { user: 'user', message: input, type: 'final_answer', thoughts: [] }
    ]);
    setInput('');

    // zera buffers
    setPendingThoughts([]);
    setCurrentThought(null);
    setModalThoughts(null);

    // 2) consome SSE
    const response = await chatStream(input, checkpointId);
    
    for await (const event of response) {
      if (event.type === 'checkpoint') {
        setCheckpointId(event.checkpoint_id);
      }
      else if (event.type === 'thoughts') {
        // cria e mostra pensamento temporário
        const thought = { user: event.agent, message: event.content, type: 'thoughts' };
        setCurrentThought(thought);
        // acumula no buffer para associar depois
        pendingRef.current.push(thought);
        console.log(pendingRef);
      }
      else if (event.type === 'final_answer') {
        
        // apaga o pensamento temporário
        setCurrentThought(null);
        const thisThoughts = [...pendingRef.current];
        pendingRef.current = []; 
        setChatLog(prev => {
          const copy = [...prev];
          const last = copy[copy.length - 1];
          

          if (last.user === 'gpt' && last.type === 'final_answer') {
            // streaming contínuo: concatena texto e preserva thoughts
            copy[copy.length - 1] = {
              ...last,
              message: last.message + event.content,
              thoughts: last.thoughts
            };
          } else {
            // nova mensagem final_answer: “flush” dos thisThoughts
            copy.push({
              user: 'gpt',
              message: event.content,
              type: 'final_answer',
              thoughts: thisThoughts
            });
          }
          return copy;
        });
        
      }
      else if (event.type === 'end') {
        // nada além de terminar o loop
        break;
      }
    }
  }

  function clearChat() {
    setChatLog([]);
    setCheckpointId(null);
    setPendingThoughts([]);
    setCurrentThought(null);
    setModalThoughts(null);
  }

  return (
    <div className="App">
      <aside className="sidemenu">
        <h1>Cage Chat</h1>
        <div className='side-menu-button' onClick={clearChat}>
          <span>+</span> New Chat
        </div>
      </aside>

      <section className='chatbox'>
        <div className='chat-log'>
          {chatLog.map((msg, i) => (
            <ChatMessage
              key={i}
              message={msg}
              onOpenModal={() => setModalThoughts(msg.thoughts)}
            />
          ))}

          {/* pensamento temporário */}
          {currentThought && (
            <ChatMessage message={currentThought} isTemporary />
          )}
        </div>

        <div className='chat-input-holder'>
          <form onSubmit={handleSubmit}>
            <input
              className='chat-input-textarea'
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder='Escreva sua mensagem aqui...'
            />
          </form>
        </div>
      </section>

      {/* Modal que mostra apenas os pensamentos da mensagem clicada */}
      {modalThoughts && (
        <Modal onClose={() => setModalThoughts(null)}>
          <h2>Pensamentos dessa resposta</h2>
          <div className="thoughts-list">
            {modalThoughts.map((t, idx) => (
              <ChatMessage key={idx} message={t} />
            ))}
          </div>
        </Modal>
      )}
    </div>
  );
}

// Component de mensagem individual
const ChatMessage = ({ message, isTemporary, onOpenModal }) => {
  const agentClass = message.user
    .toString()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-");

  const classes = ['chat-message', message.user === 'user' ? 'user' : 'gpt'];
  if (message.type === 'thoughts')    classes.push('chat-message-thought');
  if (isTemporary)                    classes.push('chat-message-temporary');

  // só exibe botão "+" se for final_answer do GPT e houver thoughts associados
  const hasThoughts = Array.isArray(message.thoughts) && message.thoughts.length > 0;
  const textWihBreaks = message.message.replace(/\\n/g, '\n');

  return (
    <div className={classes.join(' ')}>
      <div className={`chat-message-center ${message.type === 'thoughts' ? 'thoughts' : ''}`}>
        <div className={`avatar ${agentClass}`} />
        <div className="message-wrapper">
          <div className={`message ${message.type === 'thoughts' ? 'thoughts' : ''}`} style={{ whiteSpace: 'pre-line' }}>{textWihBreaks}</div>
          {message.user === 'gpt'
            && message.type === 'final_answer'
            && hasThoughts && (
            <button
              className="thoughts-button-inline"
              onClick={onOpenModal}
            >+</button>
          )}
        </div>
      </div>
    </div>
  );
};

// Modal genérico
const Modal = ({ children, onClose }) => (
  <div className="modal-overlay">
    <div className="modal modal-3d">
      <button className="modal-close" onClick={onClose}>×</button>
      {children}
    </div>
  </div>
);

export default App;
