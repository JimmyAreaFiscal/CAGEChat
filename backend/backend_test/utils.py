import json
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.utils.llm import EvaluatorLLM, EmbeddingLLM
from config import settings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

def load_test_data(filename):
    test_data_path = os.path.join(os.path.dirname(__file__), 'test_data', filename)
    with open(test_data_path, 'r') as file:
        return json.load(file)

evaluator_llm = LangchainLLMWrapper(langchain_llm=EvaluatorLLM(config=settings))
evaluator_embeddings = LangchainEmbeddingsWrapper(embeddings=EmbeddingLLM(config=settings))