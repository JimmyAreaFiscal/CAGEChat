import React from 'react';
import Sidebar from './Sidebar';

const ConversationControl = ({ onClearChat }) => {
  function clearChat() {
    if (onClearChat) onClearChat();
  }

  return <Sidebar clearChat={clearChat} />;
};

export default ConversationControl;
