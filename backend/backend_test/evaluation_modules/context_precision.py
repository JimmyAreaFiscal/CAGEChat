from backend_test.custom_schema import TestState
from backend_test.utils import evaluator_llm

from ragas import SingleTurnSample
from ragas.metrics import LLMContextPrecisionWithoutReference


context_precision = LLMContextPrecisionWithoutReference(llm=evaluator_llm)

async def evaluate_context_precision(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the context precision of the chat answer.
    """

    score = await context_precision.single_turn_ascore(state['sample'])

    return {'context_precision_score': score}


