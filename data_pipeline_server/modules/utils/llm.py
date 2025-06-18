""""
This module is responsible for creating the LLM models based on the config file. 
It is used by other modules by holding all LLM models in a single place.

"""
from config import Settings, settings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_cohere import ChatCohere, CohereEmbeddings



# Reasoning LLM:
def ReasoningLLM(config: Settings = settings):
    CHAT_MODELS_TO_USE = config.ModelSettings.CHAT_MODEL_CONFIG
    if CHAT_MODELS_TO_USE['reasoning']['type'] == "openai":
        reasoning_model = ChatOpenAI(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
    elif CHAT_MODELS_TO_USE["reasoning"]["type"] == "anthropic":
        reasoning_model = ChatAnthropic(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
    elif CHAT_MODELS_TO_USE["reasoning"]["type"] == "google":
        reasoning_model = ChatGoogleGenerativeAI(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
    elif CHAT_MODELS_TO_USE["reasoning"]["type"] == "cohere":
        reasoning_model = ChatCohere(**CHAT_MODELS_TO_USE["reasoning"]["kwargs"])
    else:
        raise ValueError(f"Invalid reasoning model type: {CHAT_MODELS_TO_USE['reasoning']['type']}")
    return reasoning_model

# General Tasks LLM:
def GeneralTasksLLM(config: Settings = settings):
    CHAT_MODELS_TO_USE = config.ModelSettings.CHAT_MODEL_CONFIG
    if CHAT_MODELS_TO_USE['general_tasks']['type'] == "openai":
        general_tasks_model = ChatOpenAI(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
    elif CHAT_MODELS_TO_USE["general_tasks"]["type"] == "anthropic":
        general_tasks_model = ChatAnthropic(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
    elif CHAT_MODELS_TO_USE["general_tasks"]["type"] == "google":
        general_tasks_model = ChatGoogleGenerativeAI(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
    elif CHAT_MODELS_TO_USE["general_tasks"]["type"] == "cohere":
        general_tasks_model = ChatCohere(**CHAT_MODELS_TO_USE["general_tasks"]["kwargs"])
    else:
        raise ValueError(f"Invalid general tasks model type: {CHAT_MODELS_TO_USE['general_tasks']['type']}")
    return general_tasks_model


# Evaluator LLM:
def EvaluatorLLM(config: Settings = settings):
    EVALUATOR_MODEL_TO_USE = config.ModelSettings.EVALUATOR_MODEL_CONFIG

    if EVALUATOR_MODEL_TO_USE['type'] == "openai":
        evaluator_model = ChatOpenAI(**EVALUATOR_MODEL_TO_USE["kwargs"])
    elif EVALUATOR_MODEL_TO_USE["type"] == "anthropic":
        evaluator_model = ChatAnthropic(**EVALUATOR_MODEL_TO_USE["kwargs"])
    else:
        raise ValueError(f"Invalid evaluator model type: {EVALUATOR_MODEL_TO_USE['type']}")
    return evaluator_model

# Set the embedding model to use
def EmbeddingLLM(config: Settings = settings):
    EMBEDDING_MODEL_TO_USE = config.ModelSettings.EMBEDDING_MODEL_CONFIG
    if EMBEDDING_MODEL_TO_USE["type"] == "openai":
        embedding_model = OpenAIEmbeddings(**EMBEDDING_MODEL_TO_USE["kwargs"])
    elif EMBEDDING_MODEL_TO_USE["type"] == "cohere":
        embedding_model = CohereEmbeddings(**EMBEDDING_MODEL_TO_USE["kwargs"])
    else:
        raise ValueError(f"Invalid embedding model type: {EMBEDDING_MODEL_TO_USE['type']}")
    return embedding_model

