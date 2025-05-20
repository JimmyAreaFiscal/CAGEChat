"""

This module is responsible for uploading documents to the vector store.

It uses the CustomLoader class to load the documents, and the vector_store module to save them.

"""

from modules.upload_docs.loader import CustomLoader
from modules.vector_store.vector_store import vectordb
from modules.utils.schemas import InputDocument
import logging

logging.basicConfig(level=logging.INFO)

def upload_documents(inputState: InputDocument):
    """
    Upload documents to the vector store.
    """
    logging.info(f"Uploading document: {inputState.file_path} - {inputState.metadata}")
    loader = CustomLoader(inputState.file_path, inputState.metadata)
    documents = loader.load()
    for doc in documents:
        vectordb.add_documents(documents)

    return {"status": "success"}

