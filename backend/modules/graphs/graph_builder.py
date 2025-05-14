"""


This module is responsible for building the graphs.

The main reason I've divided the builderrs for graphs and subgraphs is to allow the use of subgraph to create an adapter node for the main workflow.

Explanation:

The subgraphs are used in the main workflow. But, as the subgraphs have their own states, I needed to create an adapter node for each one. 

In order to modularize it better, node codes should be placed on specific folders, even if they are used as adapter. Then, to avoid cross importation (which should generate circular importation), I've separated the builders for graphs and subgraphs.

"""

from langgraph.graph import StateGraph, END 

from backend.modules.upload_docs.loader_node import upload_documents
from backend.modules.utils.schemas import AgentState
from backend.modules.answer_generation.answer_generator import generate_answer, off_topic_response, cannot_answer
from backend.modules.query_refine.question_rewriter import question_rewriter
from backend.modules.query_refine.question_classifier import question_classifier
from backend.modules.query_refine.question_decomposition import question_decomposition, subquestion_qa_retrieval
from backend.modules.query_refine.question_router import on_topic_router
from backend.modules.answer_generation.answer_routers import proceed_to_answer_router
from backend.modules.utils.schemas import InputDocument
def chat_workflow_builder() -> StateGraph:
    """
    This workflow is responsible for the main workflow of the system, responsible for the answer generation.
    """
    # Conversation workflow
    chat_workflow = StateGraph(AgentState)

    # Start with query refinement and filtering
    chat_workflow.add_node("question_rewriter", question_rewriter)
    chat_workflow.add_node("question_classifier", question_classifier)
    chat_workflow.add_node("off_topic_response", off_topic_response)
    chat_workflow.add_node("question_decomposition", question_decomposition)
    chat_workflow.set_entry_point("question_rewriter")
    chat_workflow.add_edge("question_rewriter", "question_classifier")
    chat_workflow.add_conditional_edges(
        "question_classifier",
        on_topic_router,
        {
            "question_decomposition": "question_decomposition",
            "off_topic_response": "off_topic_response"
        }
    )

    # Then, give an Q&A context to the answer generation
    chat_workflow.add_node("subquestion_qa_retrieval", subquestion_qa_retrieval)
    chat_workflow.add_node("generate_answer", generate_answer)
    chat_workflow.add_node("cannot_answer", cannot_answer)
    chat_workflow.add_edge("question_decomposition", "subquestion_qa_retrieval")
    chat_workflow.add_conditional_edges(
        "subquestion_qa_retrieval",
        proceed_to_answer_router,
        {
            "generate_answer": "generate_answer",
            "cannot_answer": "cannot_answer"
        }
    )
    
    # Then, ending the workflow
    chat_workflow.add_edge("generate_answer", END)
    chat_workflow.add_edge("cannot_answer", END)
    chat_workflow.add_edge("off_topic_response", END)
    
    return chat_workflow


def upload_documents_workflow_builder() -> StateGraph:
    """
    This workflow is responsible for the upload of documents.
    """
    upload_workflow = StateGraph(InputDocument)
    upload_workflow.add_node("upload_documents", upload_documents)
    upload_workflow.add_edge("upload_documents", END)
    upload_workflow.set_entry_point("upload_documents")
    return upload_workflow

