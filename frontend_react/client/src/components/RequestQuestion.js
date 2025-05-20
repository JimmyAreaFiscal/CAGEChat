// RequestQuestion.js
// Utility functions for question-related API requests
const API_URL = process.env.REACT_APP_API_URL ?? "http://127.0.0.1:8000";

export async function addQuestion({ question, answer, document = null, author = null }) {
  const formData = new FormData();
  formData.append('question', question);
  formData.append('answer', answer);
  if (document) formData.append('document', document);
  if (author) formData.append('author', author);

  const response = await fetch(`${API_URL}/add_question/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Erro ao adicionar questão');
  }
  return response.json();
} 