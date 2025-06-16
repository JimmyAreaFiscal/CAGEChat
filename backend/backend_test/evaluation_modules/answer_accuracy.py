from backend_test.custom_schema import TestState
from ragas import SingleTurnSample
from ragas.metrics import AnswerAccuracy    

from backend_test.utils import evaluator_llm



answer_accuracy = AnswerAccuracy(llm=evaluator_llm)

async def evaluate_answer_accuracy(state: TestState) -> TestState:
    """
    This function is responsible for evaluating the answer accuracy of the chat answer.
    """

    score = await answer_accuracy.single_turn_ascore(state['sample'])

    return {'answer_accuracy_score': score}

