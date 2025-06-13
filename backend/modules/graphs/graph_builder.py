"""


This module is responsible for building the graphs.

The main reason I've divided the builderrs for graphs and subgraphs is to allow the use of subgraph to create an adapter node for the main workflow.

Explanation:

The subgraphs are used in the main workflow. But, as the subgraphs have their own states, I needed to create an adapter node for each one. 

In order to modularize it better, node codes should be placed on specific folders, even if they are used as adapter. Then, to avoid cross importation (which should generate circular importation), I've separated the builders for graphs and subgraphs.

"""

from langgraph.graph import StateGraph, END 

from modules.upload_docs.loader_node import upload_documents
from modules.utils.schemas import AgentState
from modules.answer_generation.answer_generator import generate_answer, off_topic_response, cannot_answer
from modules.query_refine.question_rewriter import question_rewriter
from modules.query_refine.question_classifier import question_classifier
from modules.query_refine.question_decomposition import question_decomposition, subquestion_qa_retrieval
from modules.query_refine.question_router import on_topic_router
from modules.answer_generation.answer_routers import proceed_to_answer_router
from modules.utils.schemas import InputDocument
from modules.utils.general_utils import config_nodes
from config import Settings, settings


def chat_workflow_builder(config: Settings = settings) -> StateGraph:
    """
    This workflow is responsible for the main workflow of the system, responsible for the answer generation.

    Optionally accepts a Settings parameter to allow configuration of LLMs and other components.
    Pass the Settings object to all nodes/functions that require it.
    Example:
        def chat_workflow_builder(settings: Settings = default_settings) -> StateGraph:
            ...
            chat_workflow.add_node("generate_answer", lambda state: generate_answer(state, llm=GeneralTasksLLM(settings)))
            ...
    """
    # Conversation workflow
    chat_workflow = StateGraph(AgentState)

    # Start with query refinement and filtering
    chat_workflow.add_node("question_rewriter", config_nodes(question_rewriter, config))
    chat_workflow.add_node("question_classifier", config_nodes(question_classifier, config))
    chat_workflow.add_node("off_topic_response", config_nodes(off_topic_response, config))
    chat_workflow.add_node("question_decomposition", config_nodes(question_decomposition, config))
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
    chat_workflow.add_node("subquestion_qa_retrieval", config_nodes(subquestion_qa_retrieval, config))
    chat_workflow.add_node("generate_answer", config_nodes(generate_answer, config))
    chat_workflow.add_node("cannot_answer", config_nodes(cannot_answer, config))
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


def upload_documents_workflow_builder(config: Settings = settings) -> StateGraph:
    """
    This workflow is responsible for the upload of documents.
    """
    upload_workflow = StateGraph(InputDocument)
    upload_workflow.add_node("upload_documents", config_nodes(upload_documents, config))
    upload_workflow.add_edge("upload_documents", END)
    upload_workflow.set_entry_point("upload_documents")
    return upload_workflow

