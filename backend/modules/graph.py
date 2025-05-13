"""

This module is responsible for the workflow of the agents.

It uses the langgraph library to create the workflow, and the schemas module to define the state and agent state.

"""
from dotenv import load_dotenv
load_dotenv()


from langgraph.graph import add_messages, StateGraph, END 
from backend.modules.utils.schemas import AgentState, InputDocument
from langgraph.checkpoint.memory import MemorySaver
from backend.modules.upload_docs.loader_node import upload_documents
from backend.modules.answer_generation.answer_generator import generate_answer, off_topic_response, cannot_answer
from backend.modules.answer_generation.graph_routers import on_topic_router, proceed_router
from backend.modules.query_refine.question_rewriter import question_rewriter
from backend.modules.query_refine.question_classifier import question_classifier
from backend.modules.retrieval.retrieval_node import retrieval_grader, retrieve, refine_question



memory = MemorySaver()


# Conversation workflow
chat_workflow = StateGraph(AgentState)
chat_workflow.add_node("question_rewriter", question_rewriter)
chat_workflow.add_node("question_classifier", question_classifier)
chat_workflow.add_node("off_topic_response", off_topic_response)
chat_workflow.add_node("retrieve", retrieve)
chat_workflow.add_node("retrieval_grader", retrieval_grader)
chat_workflow.add_node("generate_answer", generate_answer)
chat_workflow.add_node("refine_question", refine_question)
chat_workflow.add_node("cannot_answer", cannot_answer)

chat_workflow.add_edge("question_rewriter", "question_classifier")
chat_workflow.add_conditional_edges(
    "question_classifier",
    on_topic_router,
    {
        "retrieve": "retrieve",
        "off_topic_response": "off_topic_response"
    }
)
chat_workflow.add_edge("retrieve", "retrieval_grader")
chat_workflow.add_conditional_edges(
    "retrieval_grader",
    proceed_router, 
    {
        "generate_answer": "generate_answer",
        "refine_question": "refine_question",
        "cannot_answer": "cannot_answer"
    }
)


chat_workflow.add_edge("refine_question", "retrieve")
chat_workflow.add_edge("generate_answer", END)
chat_workflow.add_edge("cannot_answer", END)
chat_workflow.add_edge("off_topic_response", END)
chat_workflow.set_entry_point("question_rewriter")
chat_graph = chat_workflow.compile(checkpointer=memory)


# Upload documents workflow
upload_workflow = StateGraph(InputDocument)
upload_workflow.add_node("upload_documents", upload_documents)
upload_workflow.add_edge("upload_documents", END)
upload_workflow.set_entry_point("upload_documents")
upload_graph = upload_workflow.compile(checkpointer=memory)


# Document upload workflow

