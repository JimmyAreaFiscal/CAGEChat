import os
import yaml
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.messages import AIMessage 
from backend.modules.utils.schemas import AgentState
from backend.modules.utils.llm import ChatLLM
from backend.modules.utils.templates import GENERATOR_PROMPT_TEMPLATE


def generate_answer(state: AgentState):
    """ 
    This node is responsible for generating a response after receiving the documents and the rephrased question from the RAG model.
    """
    print("Entering generate_answer")
    if 'messages' not in state or state['messages'] is None:
        raise ValueError("messages not found in state")
    history = state['messages']
    documents = state['documents']
    rephrased_question = state['rephrased_question']

    llm = ChatLLM
    prompt = ChatPromptTemplate.from_template(GENERATOR_PROMPT_TEMPLATE)
    rag_chain = prompt | llm 
    response = rag_chain.invoke(
        {'chat_history': history, "context": documents, "question": rephrased_question}
    )
    generation = response.content.strip() 

    state['messages'].append(AIMessage(content=generation))
    state['agent_think'] = generation
    print(f"generate_answer: Generated answer: {generation}")
    return state 

def cannot_answer(state: AgentState):
    """ 
    This node is responsible for generating a response when the RAG model does not find any relevant documents.
    """
    print("Entering cannot_answer")
    if 'messages' not in state or state['messages'] is None:
        state['messages'] = []
    
    state['messages'].append(
        AIMessage(
            content="Desculpe, não consigo responder a essa questão por não ter encontrado documentos relevantes. Por favor, reformule a questão."
        )
    )
    state['agent_think'] = "Desculpe, não consigo responder a essa questão por não ter encontrado documentos relevantes. Por favor, reformule a questão."
    return state 

def off_topic_response(state: AgentState):
    """ 
    This node is responsible for generating a response when the question is not related to the available topics.
    """
    print("Entering off_topic_response")
    if 'messages' not in state or state['messages'] is None:
        state['messages'] = []
    
    state['messages'].append(
        AIMessage(
            content="Desculpe, a questão não está relacionada aos tópicos disponíveis. Por favor, reformule a questão para um dos tópicos mencionados."
        )
    )
    state['agent_think'] = "Desculpe, a questão não está relacionada aos tópicos disponíveis. Por favor, reformule a questão para um dos tópicos mencionados."
    return state