
QUESTION_REWRITER_TEMPLATE = """ 
Você é um assistente de IA. 

Sua tarefa é gerar uma questão única do usuário, baseado no histórico de conversas. Você receberá o contexto, e retornará a questão.

Contexto: {context}
Questão: 

"""

QUESTION_CLASSIFIER_TEMPLATE = """ 
Você é um classificador que determina se a questão do usuário envolve um dos seguints tópicos:
        
1. Contabilidade Pública e Procedimentos Contábeis para o Estado do Rio Grande do Sul
2. Procedimentos administrativos no Estado do Rio Grande do Sul ou no Brasil
3. Direito Administrativo brasileiro
4. Jurisprudência sobre direito administrativo
5. Orçamentos e Direito Orçamentário e Financeiro
6. Procedimentos de auditoria pública e governamental

Se a questão não estiver relacionada a nenhum desses tópicos, responda com 'Não'. 
Se a questão estiver relacionada com pelo menos um desses tópicos, responda com "Sim"


        """

DECOMPOSITION_PROMPT_TEMPLATE = """
Você é um analista da CAGE-RS. Sua tarefa é decompor a questão do usuário em um conjunto de no máximo 3subquestões.

As subquestões devem ser independentes e separadas por linhas (newlines).

As subquestões devem ser mutuamente exclusivas e exaustivas.

Questão: {question}

Subquestões:
"""