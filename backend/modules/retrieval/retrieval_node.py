
"""
This module is responsible for generating a node for retrieving documents from the vector store.
It uses the langchain library to retrieve documents from the vector store, based on the config file (config.py). 

Then, the retrieval node is imported from the other modules.

"""

from backend.modules.retrieval.retriever import retriever
from backend.modules.utils.schemas import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.modules.utils.llm import ChatLLM 
from backend.modules.utils.schemas import GradeDocument



def retrieve(state: AgentState):
    print("Entering retrieve")
    documents = retriever.invoke(state['rephrased_question'])
    print(f"retrieve: Found {len(documents)} documents")
    state['documents'] = documents
    state['agent_think'] = f"Encontrei {len(documents)} documentos relevantes."
    return state 


def retrieval_grader(state: AgentState):
    print("Entering retrieval_grader")
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
            content=f"Questão do usuário: {state['rephrased_question']}\n\nDocumentos: \n{doc.page_content}"
        )
        grade_prompt = ChatPromptTemplate.from_messages(
            [system_message, human_message]
        )
        grader_llm = grade_prompt | structured_llm 
        result = grader_llm.invoke({})
        print(
            f"Grading document: {doc.page_content[:30]}... Score: {result.score.strip()}"
        )
        if result.score.strip().lower() == 'sim':
            relevant_docs.append(doc)
    
    state['documents'] = relevant_docs
    state['proceed_to_generate'] = len(relevant_docs) > 0
    print(f"retrieval_grader: Proceed to generate = {state['proceed_to_generate']}")
    state['agent_think'] =  f"Analisando a relevância dos documentos encontrados, encontrei {len(relevant_docs)} documentos relevantes. Vou proceder com a geração da resposta? {state['proceed_to_generate']}"
    return state 


def refine_question(state: AgentState):
    print("Entering refine_question")
    rephrase_count = state.get("rephrase_count", 0)
    if rephrase_count >= 2:
        print("Maximum rephase attempts reached")
        return state 
    question_to_refine = state['rephrased_question']
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
    print(f"refine_question: Refined question: {refined_question}")
    state['rephrased_question'] = refined_question
    state['rephrase_count'] = rephrase_count + 1
    state['agent_think'] = f"Como não foi encontrado documentos importantes para a pesquisa, refinei a questão para melhorar os resultados do Retrieval (RAG). Questão refinada: {refined_question}"
    return state 
