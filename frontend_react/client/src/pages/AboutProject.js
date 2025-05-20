import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../App.css';
import '../styles/AboutProject.css';

const sidebarItems = [
  { key: 'aboutProjectText', label: 'Sobre o Projeto' },
  { key: 'futureOfProject', label: 'Futuro do Projeto' },
  { key: 'howToContribute', label: 'Como Contribuir' },
  { key: 'ragExplanation', label: 'O que é RAG?' },
];

const content = {
  aboutProjectText: (
    <>
      <h2>Sobre o Projeto</h2>
      <p>
        Este projeto é um sistema de consulta de normas jurídicas baseado em RAG (Retrieval-Augmented Generation), desenvolvido como protótipo para um eventual uso da CAGE-RS. <br/><br/>
        Ele é baseado no programa bem sucedido do ChatTCU, cujo artigo científico pode ser consultado em: <a href="https://revista.tcu.gov.br/ojs/index.php/RTCU/article/view/2114" target="_blank" rel="noopener noreferrer">ChatTCU: Inteligência Artificial como assistente do auditor</a><br/><br/>
        <b>Não é um sistema oficial</b>, mas sim um projeto open source criado por um dos aprovados no concurso.<br/><br/>
        O objetivo é facilitar o acesso a informações jurídicas e permitir que a comunidade contribua para a melhoria contínua do assistente, até que seja possível a sua implantação oficial na CAGE-RS ou a sua utilização para apoiar uma contratação de empresas para a implantação do sistema.
      </p>
    </>
  ),
  futureOfProject: (
    <>
      <h2>Futuro do Projeto</h2>
      <p>
        Assim como o ChatTCU, pretendemos evoluir o CAGEChat em fases, começando inicialmente pela implementação de um sistema de consulta de normas jurídicas, e depois expandindo para outras funcionalidades, como análise de documentos, fundamentação de respostas, controle prévio de documentos e integração com sistemas internos.<br/><br/>
        Antes, porém, faz-se necessário que o projeto seja aprimorado e testado. Nessa primeira fase, a ideia é que seja feita: <br/><br/>
        <ul>
          <li>Construção de um banco de dados de perguntas e respostas fundamentadas</li>
          <li>Elaboração de um sistema de avaliação do sistema RAG</li>
          <li>Ampliação da base de dados de documentos (VectorStore)</li>
          <li>Otimização da arquitetura do sistema com base no resultado das avaliações e testes</li>
        </ul>
        <br/>
        O sucesso do projeto depende do engajamento da comunidade jurídica e de voluntários para alimentar e validar o sistema. <br/><br/>
        Ajude o projeto enviando perguntas e respostas fundamentadas para o CAGEChat! Clique em "Ajude o projeto" no menu principal e saiba como contribuir.
      </p>
    </>
  ),
  howToContribute: (
    <>
      <h2>Como Contribuir</h2>
      <p>
        Um sistema RAG possui uma complexidade maior que um sistema convencional, pois a sua avaliação é mais difícil e subjetiva, exigindo por diversas vezes a intervenção humana para garantir a qualidade das respostas.<br/><br/>
        Para que possa ser avaliado, um princípio básico é que haja um número significativo de perguntas que o sistema receberia, em conjunto com respostas fundamentadas como referência ("ground truth").<br/><br/>
        Contudo, elaborar perguntas e respostas fundamentadas é uma tarefa complexa, principalmente na área de atuação da CAGE-RS, o que demanda tempo e conhecimento jurídico.<br/><br/>
        Assim, você pode contribuir enviando perguntas e respostas fundamentadas, ajudando na avaliação das respostas do assistente e, eventualmente, sugerindo melhorias no código ou na arquitetura do sistema.<br/><br/>
        Entre em contato pelo repositório do projeto ou utilize a seção de "Ajude o projeto" para enviar suas contribuições.
      </p>
    </>
  ),
  ragExplanation: (
    <>
      <h2>O que é RAG?</h2>
      <p>
        RAG (Retrieval-Augmented Generation) é uma técnica de IA que combina busca em bases de dados com geração de texto, permitindo respostas mais precisas e fundamentadas.<br/><br/>
        O sistema busca informações relevantes e utiliza modelos de linguagem para gerar respostas contextualizadas.<br/><br/>
        A partir disso, é possível gerar respostas fundamentadas, por meio de inteligência artificial, a algumas perguntas, ainda que não possuam as mesmas palavras dos trechos de normas ou documentos.<br/><br/>
        O potencial desses sistemas é permitir que haja a recuperação não só de informações, mas também de conhecimentos, que vão além de simples fatos e dados.
      </p>
    </>
  ),
};

const AboutProject = () => {
  const [selected, setSelected] = useState('aboutProjectText');

  return (
    <div className="App about-project-app">
      <aside className="about-sidebar">
        <div>
          <div className="about-sidebar-header">
            <h1>CAGEChat</h1>
            <p>Sobre o Projeto</p>
          </div>
          <nav className="about-sidebar-nav">
            {sidebarItems.map(item => (
              <button
                key={item.key}
                className={selected === item.key ? 'about-sidebar-btn selected' : 'about-sidebar-btn'}
                onClick={() => setSelected(item.key)}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>
        <div className="about-sidebar-router">
          <Link to="/">Home</Link>
          <Link to="/chat">Chat</Link>
          <Link to="/question-collector">Ajude o projeto</Link>
          <Link to="/about">Sobre o projeto</Link>
        </div>
      </aside>
      <main className="about-main">
        <section className="about-content">
          {content[selected]}
        </section>
      </main>
    </div>
  );
};

export default AboutProject;
