import os
from typing import Any, Dict

from pydantic import Field
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware



class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables
    """

    # model_config = ConfigDict(extra="allow")

    CHAT_MODEL_CONFIG : Dict[str, Any] = Field(default_factory=lambda: {"type": "openai", 'kwargs': {"model": "gpt-4o-mini", "temperature": 0, }})
    EMBEDDING_MODEL_CONFIG : Dict[str, Any] = Field(default_factory=lambda: {"type": "openai", 'kwargs': {"model": "text-embedding-3-small"}})

    VECTOR_STORE_TYPE : str = "chroma"
    CHROMA_PERSIST_DIR : str = "chroma_db"
    SEARCH_TYPE : str = "mmr"
    SEARCH_KWARGS : Dict[str, Any] = Field(default_factory=lambda: {"k": 2})
    

    FINAL_NODES : list[str] = ['cannot_answer', 'off_topic_response', 'generate_answer']


    # Added for loader.py configuration
    LOADER_TYPE: str = "langchain"  # default loader type
    CHUNK_SIZE: int = 1000           # default chunk size for text splitting
    CHUNK_OVERLAP: int = 200         # default chunk overlap for text splitting

    LOCAL_DATA_DIRECTORY: str = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_data")
    )
    ALLOW_CORS: bool = False
    CORS_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: {
            "middleware_class": CORSMiddleware,
            "allow_origins": ["*"],
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "expose_headers": ["*"],
        }
    )

    # @model_validator(mode="before")
    # @classmethod
    # def _validate_values(cls, values: Dict[str, Any]) -> Dict[str, Any]:
    #     """Validate search type."""
    #     if not isinstance(values, dict):
    #         raise ValueError(
    #             f"Unexpected Pydantic v2 Validation: values are of type {type(values)}"
    #         )

    #     if not values.get("MODELS_CONFIG_PATH"):
    #         raise ValueError("MODELS_CONFIG_PATH is not set in the environment")

    #     models_config_path = os.path.abspath(values.get("MODELS_CONFIG_PATH"))

    #     if not models_config_path:
    #         raise ValueError(
    #             f"{models_config_path} does not exist. "
    #             f"You can copy models_config.sample.yaml to {settings.MODELS_CONFIG_PATH} to bootstrap config"
    #         )

    #     values["MODELS_CONFIG_PATH"] = models_config_path

    #     tfy_host = values.get("TFY_HOST")
    #     tfy_llm_gateway_url = values.get("TFY_LLM_GATEWAY_URL")
    #     if tfy_host and not tfy_llm_gateway_url:
    #         tfy_llm_gateway_url = f"{tfy_host.rstrip('/')}/api/llm"
    #         values["TFY_LLM_GATEWAY_URL"] = tfy_llm_gateway_url

    #     if not values.get("LOCAL", False) and not values.get("ML_REPO_NAME", None):
    #         raise ValueError("ML_REPO_NAME is not set in the environment")

    #     return values


settings = Settings()
