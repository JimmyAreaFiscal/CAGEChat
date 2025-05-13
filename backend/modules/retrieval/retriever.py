"""

This module is responsible for creating a retriever.
It uses the langchain library to create a retriever, based on the config file (config.py). 

Then, the retriever is imported from the other modules.

"""

from dotenv import load_dotenv
from backend.modules.vector_store.vector_store import vectordb
from backend.config import settings
load_dotenv()

SEARCH_TYPE = settings.SEARCH_TYPE
SEARCH_KWARGS = settings.SEARCH_KWARGS



retriever = vectordb.as_retriever(
    search_type=SEARCH_TYPE, 
    search_kwargs=SEARCH_KWARGS)



