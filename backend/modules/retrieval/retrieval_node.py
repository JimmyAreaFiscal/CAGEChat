import logging

"""
This module is responsible for generating a node for retrieving documents from the vector store.
It uses the langchain library to retrieve documents from the vector store, based on the config file (config.py). 

Then, the retrieval node is imported from the other modules.

"""

from backend.modules.retrieval.retriever import retriever
from backend.modules.utils.schemas import RetrievalState
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.modules.utils.llm import ChatLLM 
from backend.modules.utils.schemas import GradeDocument
from backend.modules.utils.templates import GENERATOR_RETRIEVAL_ANSWER_PROMPT_TEMPLATE
from backend.modules.utils.schemas import _avoid_spam

logging.basicConfig(level=logging.INFO)

def retrieve(state: RetrievalState):
    """
    This function is responsible for retrieving documents from the vector store.

    The retrieval question is the question to be answered by the RAG. Originally, it starts as the original question, but it can be refined and saved in the retrieval_question variable on the state. 

    """
    logging.info("Entering retrieve")

    

    retrieval_question = state.get('retrieval_question', None)

    if not retrieval_question: 
        state['retrieval_question'] = state['original_question']
        retrieval_question = state['original_question']
        
    documents = retriever.invoke(state['retrieval_question'])
    logging.info(f"retrieve: Found {len(documents)} documents")
    state['documents'] = documents
    state['agent_think'] = f"Encontrei {len(documents)} documentos relevantes."
    
    state = _avoid_spam(state)

    return state 


def retrieval_grader(state: RetrievalState):
    logging.info("Entering retrieval_grader")
    system_message = SystemMessage(
        content=""" Você é um avaliador que determina se os documentos são relevantes para a questão do usuário.
        Você só responde com 'Sim' ou 'Não'.

        Se os documentos não forem relevantes, responda com 'Não'. Se os documentos forem relevantes, responda com 'Sim'.
        """
    )
    llm = ChatLLM
    structured_llm = llm.with_structured_output(GradeDocument)

    relevant_docs = []
    for doc in state['documents']:
        human_message = HumanMessage(
            content=f"Questão do usuário: {state['retrieval_question']}\n\nDocumentos: \n{doc.page_content}"
        )
        grade_prompt = ChatPromptTemplate.from_messages(
            [system_message, human_message]
        )
        grader_llm = grade_prompt | structured_llm 
        result = grader_llm.invoke({})
        logging.info(
            f"Grading document: {doc.page_content[:30]}... Score: {result.score.strip()}"
        )
        if result.score.strip().lower() == 'sim':
            relevant_docs.append(doc)
    
    state['documents'] = relevant_docs
    state['proceed_to_generate'] = len(relevant_docs) > 0
    logging.info(f"retrieval_grader: Proceed to generate = {state['proceed_to_generate']}")
    state['agent_think'] =  f"Analisando a relevância dos documentos encontrados, encontrei {len(relevant_docs)} documentos relevantes. Vou proceder com a geração da resposta? {state['proceed_to_generate']}"
    state = _avoid_spam(state)
    return state 


def refine_question(state: RetrievalState):
    """
    This function is responsible for refining the question in order to improve the retrieval.
    """
    logging.info("Entering refine_question")

    rephrase_count = state.get("rephrase_count", 0)

    if rephrase_count >= 2:
        logging.info("Maximum rephase attempts reached")
        return state 
    
    question_to_refine = state['retrieval_question']

    system_message = SystemMessage(
        content=""" Você é um assistente que refina a questão do usuário para ser mais clara e objetiva e melhorar os resultados do Retrieval (RAG). Forneça uma versão ajustada da questão sem perder a sua essência original.
        """
    )
    human_message = HumanMessage(
        content=f"Questão original: {question_to_refine}\n\nPor favor, forneça uma versão ajustada da questão para melhorar os resultados do Retrieval (RAG)."
    )
    refine_prompt = ChatPromptTemplate.from_messages(
        [system_message, human_message]
    )
    llm = ChatLLM
    response = llm.invoke(refine_prompt.format())
    refined_question = response.content.strip()
    logging.info(f"refine_question: Refined question: {refined_question}")
    state['rephrased_question'] = refined_question
    state['rephrase_count'] = rephrase_count + 1
    state['agent_think'] = f"Como não foi encontrado documentos importantes para a pesquisa, refinei a questão para melhorar os resultados do Retrieval (RAG). Questão refinada: {refined_question}"

    state = _avoid_spam(state)
    return state 


def generate_retrieval_answer(state: RetrievalState):
    """ 
    This node is responsible for generating a response after receiving the documents and the retrieval question from the RAG model.
    """
    logging.info("Entering generate_retrieval_answer")


    question = state['retrieval_question']
    documents = state['documents']

    llm = ChatLLM
    prompt = ChatPromptTemplate.from_template(GENERATOR_RETRIEVAL_ANSWER_PROMPT_TEMPLATE)
    rag_chain = prompt | llm 
    response = rag_chain.invoke(
        {"context": documents, "question": question}
    )
    generation = response.content.strip() 

    state['answer'] = {
        'question': question,
        'answer': generation,
        'context': documents
    }
    state['agent_think'] = generation
    logging.info(f"generate_retrieval_answer: Generated retrievalanswer: {generation}")

    state['proceed_to_generate'] = True

    state = _avoid_spam(state)
    return state 


def cannot_answer_retrieval_task(state: RetrievalState):
    """ 
    This node is responsible for generating a response when the RAG model does not find any relevant documents.
    """
    logging.info("Entering cannot_answer_retrieval_task")

    state['answer'] = None
    state['agent_think'] = "Desculpe, não consigo responder a essa questão por não ter encontrado documentos relevantes. Por favor, reformule a questão."

    state['proceed_to_generate'] = False

    state = _avoid_spam(state)
    return state 

