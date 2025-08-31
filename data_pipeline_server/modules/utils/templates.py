VERIFY_DOCUMENT_TYPE_PROMPT_TEMPLATE = """ 
De acordo com o nome e o grupo do documento, retorne o tipo de documento. Assegure-se de que o tipo de documento está entre os tipos de documentos aceitos, e retorne apenas o tipo de documento, sem qualquer outra informação. 



Tipos de documentos aceitos: {allowed_document_types}

Grupo: {group}
Nome do documento: {title}

"""

GENERATE_RESUME_PROMPT_TEMPLATE = """
Você é um assistente de IA que gera resumos de um pedaço de texto baseado no seu conteúdo e nos pedaços de texto adjacentes.
O resumo deve ser um texto curto que contenha a principal ideia do pedaço de texto, e deve ter no máximo 100 caracteres. Devolva apenas o resumo, sem qualquer outra informação.

Pedaço de texto a ser resumido: <text>
{text}
</text>

Pedaços de texto adjacentes: <adjacent_texts>
{adjacent_texts}
</adjacent_texts>

Resumo:
"""

GENERATE_QUESTION_PROMPT_TEMPLATE = """
Você é um assistente de IA que gera perguntas de um pedaço de texto baseado no seu conteúdo e nos pedaços de texto adjacentes. A pergunta deve trazer a ideia principal do pedaço de texto, e deve conter no máximo 100 caracteres. Devolva apenas a pergunta, sem qualquer outra informação.

Pedaço de texto a ser perguntado: <text>
{text}
</text>

Pedaços de texto adjacentes: <adjacent_texts>
{adjacent_texts}
</adjacent_texts>

Pergunta:
"""