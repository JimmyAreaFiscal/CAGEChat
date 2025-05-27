"""

This module is responsible for the configuration of the 

It uses the pydantic_settings library to load the environment variables.

This is an idea extracted from Cognita's code, which relies on an python class to hold all the configuration.

Cognita github repo: https://github.com/truefoundry/cognita

"""


import json
import os
from typing import Any, Dict

from pydantic import Field
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable



def extract_dict_from_env(env_var: str, default_value: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Extract a dictionary from an environment variable
    """
    env_var_value = os.getenv(env_var)
    if env_var_value:
        env_var_value = json.loads(env_var_value)
    else:
        env_var_value = default_value
    return env_var_value


class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables
    """

    # model_config = ConfigDict(extra="allow")

    # Chat Model Configs 
    REASONING_MODEL_CONFIG : Dict[str, Any] = extract_dict_from_env("REASONING_CHAT_MODEL_CONFIG", {"type": "openai", 'kwargs': {"model": "gpt-4.1-2025-04-14"}})

    GENERAL_TASKS_MODEL_CONFIG : Dict[str, Any] = extract_dict_from_env("GENERAL_TASKS_CHAT_MODEL_CONFIG", {"type": "openai", 'kwargs': {"model": "gpt-4.1-nano-2025-04-14"}})

    CHAT_MODEL_CONFIG : Dict[str, Any] = {
                                            "reasoning": REASONING_MODEL_CONFIG,
                                            "general_tasks": GENERAL_TASKS_MODEL_CONFIG
                                        }
    

    EMBEDDING_MODEL_CONFIG : Dict[str, Any] = extract_dict_from_env("EMBEDDING_MODEL_CONFIG", {"type": "openai", 'kwargs': {"model": "text-embedding-3-small"}})

    
    
    VECTOR_STORE_TYPE : str = os.getenv("VECTOR_STORE_TYPE", "chroma")
    
    if VECTOR_STORE_TYPE == "qdrant":
        QDRANT_URL : str = os.getenv("QDRANT_URL")
        QDRANT_API_KEY : str = os.getenv("QDRANT_API_KEY")
        VECTORSTORE_PERSIST_DIR : dict = {"QDRANT_URL": QDRANT_URL, "QDRANT_API_KEY": QDRANT_API_KEY}
    else:
        VECTORSTORE_PERSIST_DIR : str = "chroma_db"




    SEARCH_TYPE : str = os.getenv("SEARCH_TYPE", "mmr")
    SEARCH_KWARGS : Dict[str, Any] = os.getenv("SEARCH_KWARGS", Field(default_factory=lambda: {"k": 2}))
    

    FINAL_NODES : list[str] = os.getenv("FINAL_NODES", ['cannot_answer', 'off_topic_response', 'generate_answer'])


    # Added for loader.py configuration
    LOADER_TYPE: str = "langchain"  # default loader type
    CHUNK_SIZE: int = 1000           # default chunk size for text splitting
    CHUNK_OVERLAP: int = 200         # default chunk overlap for text splitting

    LOCAL_DATA_DIRECTORY: str = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_data")
    )
    ALLOW_CORS: bool = False
    CORS_CONFIG: Dict[str, Any] = os.getenv("CORS_CONFIG", Field(
        default_factory=lambda: {
            "middleware_class": CORSMiddleware,
            "allow_origins": ["*"],
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "expose_headers": ["*"],
        }
    ))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
