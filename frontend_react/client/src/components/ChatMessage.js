import React from 'react';

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

export default ChatMessage; 