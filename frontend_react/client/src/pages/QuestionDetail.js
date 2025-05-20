import React from 'react';
import { useParams } from 'react-router-dom';

const QuestionDetail = () => {
  const { id } = useParams();
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Detalhes da Questão {id}</h1>
      <p>Aqui você pode exibir os detalhes completos da questão selecionada.</p>
    </div>
  );
};

export default QuestionDetail; 