import React, { useState, useRef, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import ChatBox from '../components/ChatBox';
import { chatStream } from '../components/RequestChat';
import '../styles/ChatPage.css';

const initialChatLog = [
  { user: 'gpt', message: 'Olá, como posso ajudar você hoje?', type: 'final_answer', thoughts: [] }
];

const initialChats = {
  1: initialChatLog
};

const initialTabs = [
  { name: 'Conversa Inicial', checkpointer_id: 1 }
];

const ChatPage = () => {

  const [chatTabs, setChatTabs] = useState(initialTabs);
  const [allChats, setAllChats] = useState(() => {
    const saved = sessionStorage.getItem('allChats');
    return saved ? JSON.parse(saved) : initialChats;
  });
  
  const [allCheckpoints, setAllCheckpoints] = useState({});
  const [currentChatId, setCurrentChatId] = useState(1);
  const [input, setInput] = useState('');
  const [currentThought, setCurrentThought] = useState(null);
  const [modalThoughts, setModalThoughts] = useState(null);
  const pendingRef = useRef([]);

  // Persist allChats in sessionStorage
  useEffect(() => {
    sessionStorage.setItem('allChats', JSON.stringify(allChats));
  }, [allChats]);

  function handleSelectChat(_, id) {
    setCurrentChatId(id);
  }

  async function handleSubmit(e) {

    e.preventDefault();
    const chatLog = allChats[currentChatId] || [];
    const newLog = [
      ...chatLog,
      { user: 'user', message: input, type: 'final_answer', thoughts: [] }
    ];
    setAllChats(prev => ({ ...prev, [currentChatId]: newLog }));
    setInput('');
    setCurrentThought(null);
    setModalThoughts(null);

    const response = await chatStream(input, allCheckpoints[currentChatId]);

    let updatedLog = newLog;

    for await (const event of response) {
      if (event.type === 'checkpoint') {

        setAllCheckpoints(prev => ({ ...prev, [currentChatId]: event.checkpoint_id }));

      } else if (event.type === 'thoughts') {

        const thought = { user: event.agent, message: event.content, type: 'thoughts' };
        setCurrentThought(thought);
        pendingRef.current.push(thought);

      } else if (event.type === 'final_answer') {

        setCurrentThought(null);
        const thisThoughts = [...pendingRef.current];
        pendingRef.current = [];
        updatedLog = [...updatedLog];
        const last = updatedLog[updatedLog.length - 1];
        if (last.user === 'gpt' && last.type === 'final_answer') {
          updatedLog[updatedLog.length - 1] = {
            ...last,
            message: last.message + event.content,
            thoughts: last.thoughts
          };

        } else {
          updatedLog.push({
            user: 'gpt',
            message: event.content,
            type: 'final_answer',
            thoughts: thisThoughts
          });
        }

        setAllChats(prev => ({ ...prev, [currentChatId]: updatedLog }));
      } else if (event.type === 'end') {
        break;
      }
    }
  }

  function handleAddChat() {
    setChatTabs(prevTabs => {

      const newId = prevTabs.length ? Math.max(...prevTabs.map(tab => tab.checkpointer_id)) + 1 : 1;
      const newTab = { name: `Conversa ${newId}`, checkpointer_id: newId };
      setAllChats(prev => ({ ...prev, [newId]: initialChatLog }));
      setAllCheckpoints(prev => ({ ...prev, [newId]: null }));
      setCurrentChatId(newId);
      setModalThoughts(null);
      return [...prevTabs, newTab];

    });
  }

  return (
    <div className="App">
      <Sidebar
        functionToCallForPreviousId={handleSelectChat}
        stringToShow="Novo Chat"
        listOfTabs={chatTabs}
        functionToCallForAddButton={handleAddChat}
      />
      <ChatBox
        chatLog={allChats[currentChatId] || []}
        currentThought={currentThought}
        input={input}
        setInput={setInput}
        handleSubmit={handleSubmit}
        modalThoughts={modalThoughts}
        setModalThoughts={setModalThoughts}
      />
    </div>
  );
};

export default ChatPage; 