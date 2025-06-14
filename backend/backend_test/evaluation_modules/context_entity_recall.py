from backend_test.custom_schema import TestState
from ragas import SingleTurnSample
from ragas.metrics import ContextEntityRecall

from backend_test.utils import evaluator_llm



context_entity_recall = ContextEntityRecall(llm=evaluator_llm)

async def evaluate_context_entity_recall(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the context entity recall of the chat answer.
    """

    score = await context_entity_recall.single_turn_ascore(state['sample'])

    return {'context_entity_recall_score': score}

