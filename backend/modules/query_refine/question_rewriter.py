from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
from backend.modules.utils.schemas import AgentState
from backend.modules.utils.llm import ChatLLM


def question_rewriter(state: AgentState) -> AgentState:
    print(f"Entering question_rrewriter with following state: {state}")


    # Reset state variables except for 'question' and 'messages'
    state['documents'] = []
    state['agent_think'] = []
    state['on_topic'] = ""
    state['rephrased_question'] = ""
    state['proceed_to_generate'] = False
    state['rephrase_count'] = 0
    
    if 'messages' not in state or state['messages'] is None:
        state['messages'] = []

    if state['question'] not in state['messages']:
        state['messages'].append(state['question'])

    if len(state['messages']) > 1:
        conversation = state['messages'][:-1]
        current_question = state['question'].content 
        messages = [
            SystemMessage(
                content='Você é um assistente que reescreve questões do usuário para ser uma única questão otimizada para o Retrieval do RAG'
                )
        ]

        messages.extend(conversation)
        messages.append(HumanMessage(content=current_question))
        rephrase_prompt = ChatPromptTemplate.from_messages(messages)
        
        llm = ChatLLM
        prompt = rephrase_prompt.format() 
        response = llm.invoke(prompt)
        better_question = response.content.strip() 
        
        print(f"question_rewriter: Rephrased question: {better_question}")
        state['rephrased_question'] = better_question
        state['agent_think'] = f"Estou eescrevendo a questão para otimizar a busca. Questão reescrita: {better_question}"
    else:
        state['rephrased_question'] = state['question'].content 
        state['agent_think'] = f"Não verifiquei necessidade de reescrever a questão."
    return state 

