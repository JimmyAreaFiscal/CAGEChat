import os
import yaml
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.messages import SystemMessage, HumanMessage
from backend.modules.utils.schemas import AgentState, GradeQuestion
from backend.modules.utils.llm import ChatLLM
from backend.modules.utils.templates import QUESTION_CLASSIFIER_TEMPLATE

def question_classifier(state: AgentState) -> AgentState:
    print("Entering question_classifier")
    system_message = SystemMessage(
        content=QUESTION_CLASSIFIER_TEMPLATE 
    )

    human_message = HumanMessage(
        content=f"Questão: {state['rephrased_question']}"
    )
    grade_prompt = ChatPromptTemplate.from_messages(
        [system_message, human_message]
    )

    llm = ChatLLM
    structured_llm = llm.with_structured_output(GradeQuestion)
    
    grader_llm = grade_prompt | structured_llm 
    result = grader_llm.invoke({})
    state['on_topic'] = result.score.strip()
    state['agent_think']= f"A questão é adequada para o contexto? {state['on_topic']}"
    print(f"question_classifier: on topic = {state['on_topic']}")

    return state 
