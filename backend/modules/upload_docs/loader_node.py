"""

This module is responsible for uploading documents to the vector store.

It uses the CustomLoader class to load the documents, and the vector_store module to save them.

"""

from backend.modules.upload_docs.loader import CustomLoader
from backend.modules.vector_store.vector_store import vectordb
from backend.modules.utils.schemas import InputDocument

def upload_documents(inputState: InputDocument):
    """
    Upload documents to the vector store.
    """
    print(f"Uploading document: {inputState.file_path} - {inputState.metadata}")
    loader = CustomLoader(inputState.file_path, inputState.metadata)
    documents = loader.load()
    for doc in documents:
        vectordb.add_documents(documents)

    return {"status": "success"}

