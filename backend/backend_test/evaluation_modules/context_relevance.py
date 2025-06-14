from backend_test.custom_schema import TestState
from ragas import SingleTurnSample
from ragas.metrics import ContextRelevance

from backend_test.utils import evaluator_llm



context_relevancy = ContextRelevance(llm=evaluator_llm)

async def evaluate_context_relevancy(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the context relevancy of the chat answer.
    """

    score = await context_relevancy.single_turn_ascore(state['sample'])
    return {'context_relevancy_score': score}

