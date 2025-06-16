from backend_test.custom_schema import TestState
from ragas import SingleTurnSample
from ragas.metrics import Faithfulness

from backend_test.utils import evaluator_llm



context_entity_recall = Faithfulness(llm=evaluator_llm)

async def evaluate_faithfulness(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the faithfulness of the chat answer.
    """

    score = await context_entity_recall.single_turn_ascore(state['sample'])
    return {'faithfulness_score': score}

