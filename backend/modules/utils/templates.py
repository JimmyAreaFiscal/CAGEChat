GENERATOR_PROMPT_TEMPLATE = """ 
Responda a questão baseado no contexto e no histórico da conversa. Leve em consideração especialmente a última questão. Ao responder, não se esqueça de fornecer a fonte da resposta, conforme o padrão abaixo, conforme tipo de documento (informado em #)

Padrão de fonte: 
 [Fonte: "<nome_documento>" - tipo de documento: "<tipo_documento>" - página: "<pagina>"] # documentos em geral
 [Fonte: "<nome_documento>" - tipo de documento: "<tipo_documento>" - título: "<título>"] # manuais
 [Fonte: "<nome_documento>" - tipo de documento: "<tipo_documento>" - artigo: "<artigo>"] # leis

Histórico: {chat_history}

Contexto: {context}

Questão: {question}

"""


GENERATOR_RETRIEVAL_ANSWER_PROMPT_TEMPLATE = """ 
Você é um assistente que responde a questão do usuário baseado no contexto fornecido. Você deve responder a questão de forma clara e objetiva, com no máximo 100 palavras.

Questão: {question}

Contexto: {context}

Resposta:
"""