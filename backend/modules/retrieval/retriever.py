"""

This module is responsible for creating a retriever.
It uses the langchain library to create a retriever, based on the config file (config.py). 

Then, the retriever is imported from the other modules.

"""

from dotenv import load_dotenv
from modules.vector_store.vector_store import VectorStore
from config import settings, Settings
load_dotenv()




def Retriever(config: Settings = settings):
    SEARCH_TYPE = settings.SearchSettings.SEARCH_TYPE
    SEARCH_KWARGS = settings.SearchSettings.SEARCH_KWARGS
    retriever = VectorStore(config).as_retriever(
        search_type=SEARCH_TYPE, 
        search_kwargs=SEARCH_KWARGS)

    return retriever



