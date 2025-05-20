import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import AboutSection from '../components/AboutSection';
import '../styles/QuestionCollector.css';

const dummyQuestions = [
  { id: 1, title: 'O que é habeas corpus?', resposta: 'Remédio constitucional para proteger a liberdade de locomoção.', fundamentacao: 'Art. 5º, LXVIII, CF' },
];

const QuestionCollector = () => {
  const [questions, setQuestions] = useState(dummyQuestions);
  const [selectedId, setSelectedId] = useState(null);
  const [form, setForm] = useState({ questao: '', resposta: '', fundamentacao: '' });
  const [showForm, setShowForm] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleSave(e) {
    e.preventDefault();
    setQuestions(prev => {
      // If editing, update; if new, add
      if (selectedId) {
        return prev.map(q =>
          q.id === selectedId
            ? { ...q, title: form.questao, resposta: form.resposta, fundamentacao: form.fundamentacao }
            : q
        );
      } else {
        return [
          ...prev,
          {
            id: prev.length ? Math.max(...prev.map(q => q.id)) + 1 : 1,
            title: form.questao,
            resposta: form.resposta,
            fundamentacao: form.fundamentacao,
          },
        ];
      }
    });
    setForm({ questao: '', resposta: '', fundamentacao: '' });
    setSelectedId(null);
    setShowForm(false);
  }

  function handleNewQuestion() {
    setForm({ questao: '', resposta: '', fundamentacao: '' });
    setSelectedId(null);
    setShowForm(true);
  }

  function handleSelect(id) {
    setSelectedId(id);
    const q = questions.find(q => q.id === id);
    setForm({
      questao: q?.title || '',
      resposta: q?.resposta || '',
      fundamentacao: q?.fundamentacao || '',
    });
    setShowForm(true);
  }

  return (
    <div className="App qc-app">
      <Sidebar
        stringToShow="Nova Questão"
        listOfTabs={questions.map(q => ({
          name: q.title,
          checkpointer_id: q.id
        }))}
        functionToCallForPreviousId={(_, id) => handleSelect(id)}
        functionToCallForAddButton={handleNewQuestion}
      />
      <main className="qc-main chatbox">
        {showForm ? (
          <form className="qc-form" onSubmit={handleSave}>
            <label className="qc-label">
              Questão
              <textarea
                name="questao"
                value={form.questao}
                onChange={handleChange}
                className="qc-input"
                rows={2}
                required
              />
            </label>
            <label className="qc-label">
              Resposta
              <textarea
                name="resposta"
                value={form.resposta}
                onChange={handleChange}
                className="qc-input"
                rows={3}
                required
              />
            </label>
            <label className="qc-label">
              Fundamentação, se tiver
              <textarea
                name="fundamentacao"
                value={form.fundamentacao}
                onChange={handleChange}
                className="qc-input"
                rows={2}
              />
            </label>
            <div className="qc-form-actions">
              <button type="submit" className="qc-btn qc-btn-save">Salvar Questão</button>
              <button type="button" className="qc-btn qc-btn-erase" onClick={() => setShowForm(false)}>Cancelar</button>
            </div>
          </form>
        ) : (
          <AboutSection />
        )}
      </main>
    </div>
  );
};

export default QuestionCollector; 