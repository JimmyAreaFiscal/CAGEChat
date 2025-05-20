import React from 'react';
import ChatMessage from './ChatMessage';
import Modal from './Modal';

const ChatBox = ({ chatLog, currentThought, input, setInput, handleSubmit, modalThoughts, setModalThoughts }) => (
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
  </section>
);

export default ChatBox; 