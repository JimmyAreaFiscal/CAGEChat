from backend_test.custom_schema import TestState
from ragas import SingleTurnSample
from ragas.metrics import ResponseRelevancy

from backend_test.utils import evaluator_llm, evaluator_embeddings



response_relevancy = ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)

async def evaluate_response_relevancy(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the response relevancy of the chat answer.
    """

    score = await response_relevancy.single_turn_ascore(state['sample'])
    return {'response_relevancy_score': score}

