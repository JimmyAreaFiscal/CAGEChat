"""

This module is responsible for uploading documents to the vector store.

It uses the CustomLoader class to load the documents, and the vector_store module to save them.

"""

from config import Settings, settings
from modules.vector_store.vector_store import VectorStore
from modules.utils.schemas import InputDocument
import logging
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO)


def filter_complex_metadata(metadata):
    return {
        k: v
        for k, v in metadata.items()
        if isinstance(v, (str, int, float, bool)) or v is None
    }

def upload_documents(state: InputDocument, config: Settings = settings):
    """
    Upload documents to the vector store.
    """
    logging.info(f"Uploading document: {state.title} - {state.group} - {state.area}")
    
    if config.VectorStoreSettings.VECTOR_STORE_TYPE == "chroma":
        logging.info("Using ChromaDB")
        filtered_documents = [
            Document(
                page_content=doc.page_content,
                metadata=filter_complex_metadata(doc.metadata)
            )
            for doc in state.documents_processed
        ]
        VectorStore(config).add_documents(filtered_documents)

    else:
        logging.info("Using other vector store")
        VectorStore(config).add_documents(state.documents_processed)

    return {"status": "success"}

