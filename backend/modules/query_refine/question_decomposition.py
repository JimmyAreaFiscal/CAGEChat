"""
This modules contains the logic for refining the question by using subqueries pipeline.

The question is decomposed into a list of subqueries related to the main question, each one being answered by subRAG systems, in order to improve the qualiy of the context retrieved.

This pipeline is explained in the following article: 

Advanced Retrieval Technique for Better RAGs - by Thuwarakesh Murallie

https://medium.com/data-science/advanced-retrieval-technique-for-better-rags-c53e1b03c183

"""

from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.modules.utils.templates import DECOMPOSITION_PROMPT_TEMPLATE
from backend.modules.utils.schemas import DecomposedQuestion, AgentState
from backend.modules.utils.llm import ChatLLM
from backend.modules.graphs.subgraph_builder import retrieval_workflow_builder
import asyncio


def question_decomposition(state: AgentState) -> List[str]:
    """
    Decompose the question into a list of subqueries related. 
    """
    question = state['rephrased_question']
    prompt = ChatPromptTemplate.from_template(DECOMPOSITION_PROMPT_TEMPLATE)
    llm_with_structured_output = ChatLLM.with_structured_output(DecomposedQuestion)
    llm = prompt | llm_with_structured_output
    result = llm.invoke({"question": question})
    
    state['subquestions'] = result.subquestions
    return state


async def subquestion_qa_retrieval(state: AgentState) -> AgentState:
    """
    This function is responsible for answering the subquestions using the RAG subgraph.
    """

    retrieval_workflow = retrieval_workflow_builder()
    retrieval_graph = retrieval_workflow.compile()

    subquestions = state['subquestions']
    qa_context = [
        retrieval_graph.ainvoke({"original_question": q})
        for q in subquestions
    ]
    completed = await asyncio.gather(*qa_context)
    final_qa_context = []
    for qa in completed:
        if qa.get('answer', None):
           final_qa_context.append(qa['answer']) 
    state['qa_context'] = final_qa_context

    return state



