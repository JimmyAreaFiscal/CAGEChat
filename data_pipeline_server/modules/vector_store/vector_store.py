"""
This module is responsible for creating a vector store. 
It uses the langchain library to create a vector store of a given type, based on the config file (config.py). 

Then, the vector store is imported from the other modules.

"""

from modules.utils.llm import EmbeddingLLM
from langchain_community.vectorstores import Chroma, FAISS, Milvus
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import VectorParams, Distance
from dotenv import load_dotenv
from config import Settings, settings


load_dotenv()

def VectorStore(config: Settings = settings):
    VECTOR_STORE_TYPE = config.VectorStoreSettings.VECTOR_STORE_TYPE

    embeddings_func = EmbeddingLLM(config)

    if VECTOR_STORE_TYPE == "chroma":
        CHROMA_DIR = config.VectorStoreSettings.VECTORSTORE_PERSIST_DIR
        vectordb = Chroma(
                    embedding_function=embeddings_func,
                    persist_directory=CHROMA_DIR
                )

    elif VECTOR_STORE_TYPE == "faiss":
        FAISS_DIR = config.VectorStoreSettings.VECTORSTORE_PERSIST_DIR
        vectordb = FAISS(embedding_function=embeddings_func, index_to_docstore_id={})

    elif VECTOR_STORE_TYPE == "milvus":
        MILVUS_DIR = config.VectorStoreSettings.VECTORSTORE_PERSIST_DIR
        vectordb = Milvus(embedding_function=embeddings_func, index_to_docstore_id={})

    # Adicione Qdrant 
    elif VECTOR_STORE_TYPE == "qdrant":
        from qdrant_client import QdrantClient

        client = QdrantClient(
            url=config.VectorStoreSettings.VECTORSTORE_PERSIST_DIR["QDRANT_URL"],
            api_key=config.VectorStoreSettings.VECTORSTORE_PERSIST_DIR["QDRANT_API_KEY"]
        )

        # Verifique se o collection_name existe. Se não existir, crie uma nova coleção
        if not client.collection_exists(collection_name="cagers-server-collection"):
            client.create_collection(collection_name="cagers-server-collection", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))

        vectordb = QdrantVectorStore(client=client, embedding=embeddings_func, collection_name="cagers-server-collection")

    else:
        raise ValueError(f"Invalid vector store type: {VECTOR_STORE_TYPE}")
    return vectordb






