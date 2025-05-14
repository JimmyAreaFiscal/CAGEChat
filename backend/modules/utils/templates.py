GENERATOR_PROMPT_TEMPLATE = """ Responda a questão baseado no contexto e no histórico da conversa. Leve em consideração especialmente a última questão. 

Histórico: {chat_history}

Contexto: {context}

Questão: {question}

"""

QUESTION_REWRITER_TEMPLATE = """ 
Você é um assistente que reescreve questões do usuário para ser uma única questão otimizada para o Retrieval do RAG, de forma a considerar todo o contexto da conversa. 

Questão: {question}

"""

QUESTION_CLASSIFIER_TEMPLATE = """ 
Você é um classificador que determina se a questão do usuário envolve um dos seguints tópicos:
        
1. Contabilidade Pública e Procedimentos Contábeis para o Estado do Rio Grande do Sul
2. Procedimentos administrativos no Estado do Rio Grande do Sul ou no Brasil
3. Direito Administrativo brasileiro
4. Jurisprudência sobre direito administrativo
5. Orçamentos e Direito Orçamentário e Financeiro

Se a questão não estiver relacionada a nenhum desses tópicos, responda com 'Não'. Se a questão estiver relacionada com pelo menos um desses tópicos, responda com "Sim"
        """

DECOMPOSITION_PROMPT_TEMPLATE = """
Você é um analista da CAGE-RS. Sua tarefa é decompor a questão do usuário em um conjunto de subquestões.

As subquestões devem ser independentes e separadas por linhas (newlines).

As subquestões devem ser mutuamente exclusivas e exaustivas.

Questão: {question}

Subquestões:
"""

GENERATOR_RETRIEVAL_ANSWER_PROMPT_TEMPLATE = """ 
Você é um assistente que responde a questão do usuário baseado no contexto fornecido. Você deve responder a questão de forma clara e objetiva, com no máximo 100 palavras.

Questão: {question}

Contexto: {context}

Resposta:
"""