"""

This module is responsible for coding the builders for subgraphs

"""

from langgraph.graph import StateGraph, END 
from backend.modules.utils.schemas import RetrievalState
from backend.modules.retrieval.retrieval_node import retrieval_grader, retrieve, refine_question, generate_retrieval_answer, cannot_answer_retrieval_task
from backend.modules.retrieval.retrieval_edge import proceed_retrieval_router

# Subgraph for Retrieval
def retrieval_workflow_builder() -> StateGraph:
    """
    This subgraph is responsible for modularizing the retrieval process. 

    It is responsible for retrieving the documents from the RAG, grading them and refining the question if necessary.

    This is an attempt to use this subgraph for more than one time in the main workflow, in order to allow subqueries to be answered before the main question.
    
    """
    retrieval_workflow = StateGraph(RetrievalState)
    retrieval_workflow.add_node("retrieve", retrieve)
    retrieval_workflow.add_node("retrieval_grader", retrieval_grader)
    retrieval_workflow.add_node("refine_question", refine_question)
    retrieval_workflow.add_node("generate_retrieval_answer", generate_retrieval_answer)
    retrieval_workflow.add_node("cannot_answer_retrieval_task", cannot_answer_retrieval_task)
    retrieval_workflow.set_entry_point("retrieve")


    retrieval_workflow.add_edge("retrieve", "retrieval_grader")
    retrieval_workflow.add_conditional_edges(
        "retrieval_grader",
        proceed_retrieval_router,
        {
            "generate_retrieval_answer": "generate_retrieval_answer",
            "refine_question": "refine_question",
            "cannot_answer_retrieval_task": "cannot_answer_retrieval_task"
        }
    )
    retrieval_workflow.add_edge("refine_question", "retrieve")
    retrieval_workflow.add_edge("generate_retrieval_answer", END)
    retrieval_workflow.add_edge("cannot_answer_retrieval_task", END)
    
    
    return retrieval_workflow




