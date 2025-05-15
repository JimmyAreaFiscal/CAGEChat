"""

This module is responsible for verifying if the question can be answered by the CAGEChat system or not. 

General questions are not answered by the CAGEChat system, because they are not related to the CAGE-RS. This is an attempt to avoid misleading uses of the system and efficiency (due to not using tokens and LLM calls to return 'cannot_answer' messages).

For example, the question "Como posso me tornar um melhor atleta?" is not related to the CAGE-RS, so it is not answered by the CAGEChat system. 

"""
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.messages import SystemMessage, HumanMessage
from backend.modules.utils.schemas import AgentState, GradeQuestion
from backend.modules.utils.llm import ChatLLM
from backend.modules.utils.templates import QUESTION_CLASSIFIER_TEMPLATE
import logging

logging.basicConfig(level=logging.INFO)

def question_classifier(state: AgentState) -> AgentState:
    logging.info("Entering question_classifier")
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
    logging.info(f"question_classifier: on topic = {state['on_topic']}")

    return state 
