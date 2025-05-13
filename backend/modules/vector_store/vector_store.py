"""
This module is responsible for creating a vector store. 
It uses the langchain library to create a vector store of a given type, based on the config file (config.py). 

Then, the vector store is imported from the other modules.

"""

from backend.modules.utils.llm import EmbeddingLLM
from langchain_community.vectorstores import Chroma, FAISS, Milvus
from dotenv import load_dotenv
from backend.config import settings


load_dotenv()


VECTOR_STORE_TYPE = settings.VECTOR_STORE_TYPE

embeddings_func = EmbeddingLLM

if VECTOR_STORE_TYPE == "chroma":
    CHROMA_DIR = settings.CHROMA_PERSIST_DIR
    vectordb = Chroma(
                embedding_function=embeddings_func,
                persist_directory=CHROMA_DIR
            )

elif VECTOR_STORE_TYPE == "faiss":
    FAISS_DIR = settings.FAISS_PERSIST_DIR
    vectordb = FAISS(embedding_function=embeddings_func, index_to_docstore_id={})

elif VECTOR_STORE_TYPE == "milvus":
    MILVUS_DIR = settings.MILVUS_PERSIST_DIR
    vectordb = Milvus(embedding_function=embeddings_func, index_to_docstore_id={})

else:
    raise ValueError(f"Invalid vector store type: {VECTOR_STORE_TYPE}")






