""""
This module is responsible for creating the LLM models based on the config file. 
It is used by other modules by holding all LLM models in a single place.

"""
from backend.config import settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_cohere import ChatCohere, CohereEmbeddings

CHAT_MODEL_TO_USE = settings.CHAT_MODEL_CONFIG
EMBEDDING_MODEL_TO_USE = settings.EMBEDDING_MODEL_CONFIG


# Set the LLM model to use
if CHAT_MODEL_TO_USE["type"] == "openai":
    ChatLLM = ChatOpenAI(**CHAT_MODEL_TO_USE["kwargs"])
elif CHAT_MODEL_TO_USE["type"] == "anthropic":
    ChatLLM = ChatAnthropic(**CHAT_MODEL_TO_USE["kwargs"])
elif CHAT_MODEL_TO_USE["type"] == "google":
    ChatLLM = ChatGoogleGenerativeAI(**CHAT_MODEL_TO_USE["kwargs"])
elif CHAT_MODEL_TO_USE["type"] == "cohere":
    ChatLLM = ChatCohere(**CHAT_MODEL_TO_USE["kwargs"])


# Set the embedding model to use
if EMBEDDING_MODEL_TO_USE["type"] == "openai":
    EmbeddingLLM = OpenAIEmbeddings(**EMBEDDING_MODEL_TO_USE["kwargs"])
elif EMBEDDING_MODEL_TO_USE["type"] == "cohere":
    EmbeddingLLM = CohereEmbeddings(**EMBEDDING_MODEL_TO_USE["kwargs"])

