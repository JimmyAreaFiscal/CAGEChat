import React from 'react';

const AboutSection = () => (
  <div className="qc-about-card">
    <h2 className="qc-about-title">Sobre o Coletor de Questões</h2>
    <p className="qc-about-desc">
      Este é um projeto de Sistema RAG (Retrieval-Augmented Generation) para consultas de normas jurídicas no âmbito da CAGE-RS. Não é, contudo, um sistema oficial, massim um projeto de código aberto feito por um dos aprovados no concurso. <br/><br/>

      Por não ter recursos o suficiente, dependemos de apoio de voluntários para criar um banco de dados de perguntas e respostas fundamentadas, que será usado para poder fazer as avaliações do sistema RAG e, consequentemente, melhorar a qualidade das respostas do CAGEChat. <br/><br/>

      Ajude o projeto CAGEChat enviando questões e respostas fundamentadas para o CAGEChat.!<br/><br/>
      Suas contribuições ajudam a melhorar a base de conhecimento do assistente.<br/><br/>
      Clique em <b>"Nova Questão"</b> para enviar uma nova pergunta e resposta fundamentada.
    </p>
  </div>
);

export default AboutSection; 