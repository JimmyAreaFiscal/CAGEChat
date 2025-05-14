"""

This module is responsible for rewriting the question to allow the system to use the historical conversations.

On doing so, the system resumes the conversation context and the last question asked to find out the user's intent.

"""


from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
from backend.modules.utils.schemas import AgentState
from backend.modules.utils.llm import ChatLLM
from backend.modules.utils.templates import QUESTION_REWRITER_TEMPLATE

def question_rewriter(state: AgentState) -> AgentState:
    """
    This function is responsible for rewriting the question to allow the system to use the historical conversations.
    """
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
                content=QUESTION_REWRITER_TEMPLATE
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
        state['agent_think'] = f"Estou reescrevendo a questão para otimizar a busca. Questão reescrita: {better_question}"
    else:
        state['rephrased_question'] = state['question'].content 
        state['agent_think'] = f"Não verifiquei necessidade de reescrever a questão."
    return state 

