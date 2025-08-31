


from modules.embedding_storage.legislation_processing import chunking_by_article
from modules.embedding_storage.preprocessing import verify_document_type, document_type_router
from modules.utils.general_utils import config_nodes
from modules.utils.schemas import InputDocument
from langgraph.graph import StateGraph, END
from config import Settings, settings
from modules.embedding_storage.augmented_context_generator import generate_resume, generate_question
from modules.embedding_storage.upload_to_vectorstore import upload_documents


def upload_documents_workflow_builder(config: Settings = settings) -> StateGraph:
    """
    This workflow is responsible for the upload of documents.
    """
    upload_workflow = StateGraph(InputDocument)

    upload_workflow.add_node("verify_document_type", config_nodes(verify_document_type, config))
    upload_workflow.add_node("chunking_by_article", config_nodes(chunking_by_article, config))
    upload_workflow.add_node("generate_resume", config_nodes(generate_resume, config))
    upload_workflow.add_node("generate_question", config_nodes(generate_question, config))
    upload_workflow.add_node("upload_documents", config_nodes(upload_documents, config))
    upload_workflow.add_conditional_edges(
        "verify_document_type",
        document_type_router,
        {
            "chunking_by_article": "chunking_by_article"
        }
    )

    upload_workflow.add_edge("chunking_by_article", "generate_resume")
    upload_workflow.add_edge("generate_resume", "generate_question") 

    upload_workflow.add_edge("generate_question", "upload_documents") 
    upload_workflow.add_edge("upload_documents", END)

    upload_workflow.set_entry_point("verify_document_type")
    return upload_workflow
