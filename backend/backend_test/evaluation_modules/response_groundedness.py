from backend_test.custom_schema import TestState
from ragas import SingleTurnSample
from ragas.metrics import ResponseGroundedness

from backend_test.utils import evaluator_llm



response_groundness = ResponseGroundedness(llm=evaluator_llm)

async def evaluate_response_groundness(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the response groundedness of the chat answer.
    """

    score = await response_groundness.single_turn_ascore(state['sample'])
    return {'response_groundness_score': score}

