""""
This module is responsible for creating the LLM models based on the config file. 
It is used by other modules by holding all LLM models in a single place.

"""
from config import settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_cohere import ChatCohere, CohereEmbeddings

CHAT_MODELS_TO_USE = settings.ModelSettings.CHAT_MODEL_CONFIG
EMBEDDING_MODEL_TO_USE = settings.ModelSettings.EMBEDDING_MODEL_CONFIG


# Reasoning LLM:

if CHAT_MODELS_TO_USE['reasoning']['type'] == "openai":
    ReasoningLLM = ChatOpenAI(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
elif CHAT_MODELS_TO_USE["reasoning"]["type"] == "anthropic":
    ReasoningLLM = ChatAnthropic(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
elif CHAT_MODELS_TO_USE["reasoning"]["type"] == "google":
    ReasoningLLM = ChatGoogleGenerativeAI(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
elif CHAT_MODELS_TO_USE["reasoning"]["type"] == "cohere":
    ReasoningLLM = ChatCohere(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
else:
    raise ValueError(f"Invalid reasoning model type: {CHAT_MODELS_TO_USE['reasoning']['type']}")

# General Tasks LLM:

if CHAT_MODELS_TO_USE['general_tasks']['type'] == "openai":
    GeneralTasksLLM = ChatOpenAI(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
elif CHAT_MODELS_TO_USE["general_tasks"]["type"] == "anthropic":
    GeneralTasksLLM = ChatAnthropic(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
elif CHAT_MODELS_TO_USE["general_tasks"]["type"] == "google":
    GeneralTasksLLM = ChatGoogleGenerativeAI(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
elif CHAT_MODELS_TO_USE["general_tasks"]["type"] == "cohere":
    GeneralTasksLLM = ChatCohere(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
else:
    raise ValueError(f"Invalid general tasks model type: {CHAT_MODELS_TO_USE['general_tasks']['type']}")





# Set the embedding model to use
if EMBEDDING_MODEL_TO_USE["type"] == "openai":
    EmbeddingLLM = OpenAIEmbeddings(**EMBEDDING_MODEL_TO_USE["kwargs"])
elif EMBEDDING_MODEL_TO_USE["type"] == "cohere":
    EmbeddingLLM = CohereEmbeddings(**EMBEDDING_MODEL_TO_USE["kwargs"])

