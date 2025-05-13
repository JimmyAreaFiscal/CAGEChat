GENERATOR_PROMPT_TEMPLATE = """ Responda a questão baseado no contexto e no histórico da conversa. Leve em consideração especialmente a última questão. 

Histórico: {chat_history}

Contexto: {context}

Questão: {question}

"""

QUESTION_CLASSIFIER_TEMPLATE = """ 
Você é um classificador que determina se a questão do usuário envolve um dos seguints tópicos:
        
1. Contabilidade Pública e Procedimentos Contábeis
2. Procedimentos administrativos no Estado do Rio Grande do Sul ou no Brasil
3. Direito Administrativo brasileiro
4. Jurisprudência sobre direito administrativo
5. Orçamentos e Direito Orçamentário e Financeiro

Se a questão não estiver relacionada a nenhum desses tópicos, responda com 'Não'. Se a questão estiver relacionada com pelo menos um desses tópicos, responda com "Sim"
        """

